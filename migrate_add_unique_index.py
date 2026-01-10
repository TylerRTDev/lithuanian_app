import sqlite3

DB_PATH = "app.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(cards)")
    cols = [row[1] for row in cur.fetchall()]  # row[1] = column name

    if "pronunciation" not in cols:
        cur.execute("ALTER TABLE cards ADD COLUMN pronunciation TEXT")
        conn.commit()
        print("✅ Added pronunciation column to cards.")
    else:
        print("ℹ️ pronunciation column already exists. No changes made.")

    conn.close()

if __name__ == "__main__":
    main()
