DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS progress;

CREATE TABLE cards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lt TEXT NOT NULL,
  en TEXT NOT NULL,
  category TEXT NOT NULL DEFAULT '01_greetings'
);

-- progress tracks what the user has seen (study mode)
CREATE TABLE progress (
  card_id INTEGER PRIMARY KEY,
  seen_count INTEGER NOT NULL DEFAULT 0,
  last_seen TEXT,
  FOREIGN KEY (card_id) REFERENCES cards (id)
);
