from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from flask import Flask, g, jsonify, render_template, request

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")


# ---------------- DB helpers ----------------
def get_db() -> sqlite3.Connection:
    if "db" not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create DB if missing (only for first run)."""
    db = sqlite3.connect(DB_PATH)

    # If you still have schema.sql, we can run it on first creation.
    # This version creates tables directly to avoid schema mismatch.
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS cards (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          lt TEXT NOT NULL,
          en TEXT NOT NULL,
          category TEXT NOT NULL DEFAULT '01_greetings',
          pronunciation TEXT
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS progress (
          card_id INTEGER PRIMARY KEY,
          seen_count INTEGER NOT NULL DEFAULT 0,
          last_seen TEXT,
          FOREIGN KEY (card_id) REFERENCES cards (id)
        )
        """
    )

    # Tiny seed (only if DB is empty)
    existing = db.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
    if existing == 0:
        starter = [
            ("labas", "hello (informal)", "01_greetings", "LAH-bahs"),
            ("ačiū", "thank you|thanks", "01_greetings", "AH-choo"),
            ("prašau", "please / you're welcome", "01_greetings", "PRAH-shau"),
            ("taip", "yes", "03_basics", "tahp"),
            ("ne", "no", "03_basics", "neh"),
        ]
        db.executemany(
            "INSERT INTO cards (lt, en, category, pronunciation) VALUES (?, ?, ?, ?)",
            starter,
        )

    db.commit()
    db.close()


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())


# ---------------- Routes ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/categories", methods=["GET"])
def categories():
    db = get_db()
    rows = db.execute("SELECT DISTINCT category FROM cards ORDER BY category ASC").fetchall()
    return jsonify({"categories": [r["category"] for r in rows]})


@app.route("/api/next", methods=["GET"])
def next_card():
    """
    Returns the next card for the chosen category.
    We return lt + en + pronunciation so Learn/Test can both use it.
    """
    category = request.args.get("category")
    db = get_db()

    if not category:
        first = db.execute("SELECT category FROM cards ORDER BY category ASC LIMIT 1").fetchone()
        if first is None:
            return jsonify({"error": "No cards found in database."}), 404
        category = first["category"]

    row = db.execute(
        """
        SELECT
          c.id, c.lt, c.en, c.category,
          COALESCE(c.pronunciation, '') AS pronunciation,
          COALESCE(p.seen_count, 0) AS seen_count
        FROM cards c
        LEFT JOIN progress p ON p.card_id = c.id
        WHERE c.category = ?
        ORDER BY COALESCE(p.seen_count, 0) ASC, RANDOM()
        LIMIT 1
        """,
        (category,),
    ).fetchone()

    if row is None:
        return jsonify({"error": f"No cards found for category: {category}"}), 404

    return jsonify(
        {
            "id": row["id"],
            "lt": row["lt"],
            "en": row["en"],
            "category": row["category"],
            "pronunciation": row["pronunciation"],
            "seen_count": row["seen_count"],
        }
    )


@app.route("/api/seen", methods=["POST"])
def mark_seen():
    """Called when the user reveals in Learn mode (and optionally after answer in Test)."""
    data = request.get_json(force=True)
    card_id = data.get("card_id")
    if not card_id:
        return jsonify({"error": "card_id is required"}), 400

    db = get_db()
    now = utc_now_iso()

    exists = db.execute("SELECT card_id FROM progress WHERE card_id = ?", (card_id,)).fetchone()
    if exists is None:
        db.execute(
            "INSERT INTO progress (card_id, seen_count, last_seen) VALUES (?, 1, ?)",
            (card_id, now),
        )
    else:
        db.execute(
            "UPDATE progress SET seen_count = seen_count + 1, last_seen = ? WHERE card_id = ?",
            (now, card_id),
        )

    db.commit()
    return jsonify({"ok": True})


@app.route("/api/check", methods=["POST"])
def check_answer():
    """
    Test mode endpoint:
    - checks typed answer against the card's en (supports synonyms separated by |)
    - returns correct/incorrect + correct answer
    Score is handled client-side (only in Test mode).
    """
    data = request.get_json(force=True)
    card_id = data.get("card_id")
    answer = data.get("answer", "")

    if not card_id:
        return jsonify({"error": "card_id is required"}), 400

    db = get_db()
    row = db.execute(
        "SELECT en FROM cards WHERE id = ?",
        (card_id,),
    ).fetchone()

    if row is None:
        return jsonify({"error": "Card not found"}), 404

    accepted = [normalize(x) for x in str(row["en"]).split("|")]
    given = normalize(answer)

    is_correct = given in accepted
    return jsonify({"is_correct": is_correct, "correct_answer": row["en"]})


@app.route("/api/stats", methods=["GET"])
def stats():
    category = request.args.get("category")
    db = get_db()

    if category:
        total_in_cat = db.execute(
            "SELECT COUNT(*) AS n FROM cards WHERE category = ?",
            (category,),
        ).fetchone()["n"]

        unique_seen_in_cat = db.execute(
            """
            SELECT COUNT(*) AS n
            FROM progress p
            JOIN cards c ON c.id = p.card_id
            WHERE c.category = ? AND p.seen_count > 0
            """,
            (category,),
        ).fetchone()["n"]
    else:
        total_in_cat = 0
        unique_seen_in_cat = 0

    unique_seen_total = db.execute(
        "SELECT COUNT(*) AS n FROM progress WHERE seen_count > 0"
    ).fetchone()["n"]

    total_cards = db.execute("SELECT COUNT(*) AS n FROM cards").fetchone()["n"]

    return jsonify(
        {
            "category": category,
            "total_in_category": total_in_cat,
            "unique_seen_in_category": unique_seen_in_cat,
            "unique_seen_total": unique_seen_total,
            "total_cards": total_cards,
        }
    )


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(debug=True)
