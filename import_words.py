import json
import sqlite3

DB_PATH = "app.db"
JSON_PATH = "words.json"

def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        words = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    inserted = 0
    updated = 0
    skipped = 0

    for w in words:
        lt = (w.get("lt") or "").strip()
        en = (w.get("en") or "").strip()
        category = (w.get("category") or "").strip()
        pronunciation = (w.get("pronunciation") or "").strip()

        if not lt or not en or not category:
            skipped += 1
            continue

        cur.execute("SELECT id, en, COALESCE(pronunciation, '') FROM cards WHERE lt = ? AND category = ?", (lt, category))
        row = cur.fetchone()

        if row is None:
            cur.execute(
                "INSERT INTO cards (lt, en, category, pronunciation) VALUES (?, ?, ?, ?)",
                (lt, en, category, pronunciation or None),
            )
            inserted += 1
        else:
            card_id, existing_en, existing_pron = row
            changed = False

            if existing_en != en:
                cur.execute("UPDATE cards SET en = ? WHERE id = ?", (en, card_id))
                changed = True

            if (existing_pron or "") != (pronunciation or ""):
                cur.execute("UPDATE cards SET pronunciation = ? WHERE id = ?", (pronunciation or None, card_id))
                changed = True

            if changed:
                updated += 1
            else:
                skipped += 1

    conn.commit()
    conn.close()

    print(f"✅ Import done. Inserted: {inserted}, Updated: {updated}, Unchanged/Skipped: {skipped}")

if __name__ == "__main__":
    main()
