# Lithuanian Flashcard Learning App 🇱🇹🌿

A simple, beginner-friendly language learning web app inspired by flashcards.  
The app helps users learn Lithuanian vocabulary through **Learn** and **Test** modes, with pronunciation hints and category-based progression.

Built with **Python (Flask)**, **SQLite**, **HTML/CSS**, and **JavaScript**.

---

## Features

- 📚 **500 Lithuanian words** organised by category and difficulty
- 👀 **Learn mode**
  - See the Lithuanian word
  - Reveal the English translation
  - View a beginner-friendly pronunciation hint
- ✍️ **Test mode**
  - Type the English translation
  - Get instant feedback
  - Score tracking (only in Test mode)
- 🗂️ Category selection (e.g. greetings, basics, food, verbs)
- 🧠 Progress stored locally in a database
- 🌿 Soft, calm, nature-inspired UI

---

## Tech Stack

**Backend**
- Python
- Flask
- SQLite

**Frontend**
- HTML
- CSS
- Vanilla JavaScript

**Data**
- `words.json` – source of truth for vocabulary and pronunciation

---

## Project Structure

# Lithuanian Flashcard Learning App 🇱🇹🌿

A simple, beginner-friendly language learning web app inspired by flashcards.  
The app helps users learn Lithuanian vocabulary through **Learn** and **Test** modes, with pronunciation hints and category-based progression.

Built with **Python (Flask)**, **SQLite**, **HTML/CSS**, and **JavaScript**.

---

## Features

- 📚 **500 Lithuanian words** organised by category and difficulty
- 👀 **Learn mode**
  - See the Lithuanian word
  - Reveal the English translation
  - View a beginner-friendly pronunciation hint
- ✍️ **Test mode**
  - Type the English translation
  - Get instant feedback
  - Score tracking (only in Test mode)
- 🗂️ Category selection (e.g. greetings, basics, food, verbs)
- 🧠 Progress stored locally in a database
- 🌿 Soft, calm, nature-inspired UI

---

## Tech Stack

**Backend**
- Python
- Flask
- SQLite

**Frontend**
- HTML
- CSS
- Vanilla JavaScript

**Data**
- `words.json` – source of truth for vocabulary and pronunciation

---

## Project Structure

# Lithuanian Flashcard Learning App 🇱🇹🌿

A simple, beginner-friendly language learning web app inspired by flashcards.  
The app helps users learn Lithuanian vocabulary through **Learn** and **Test** modes, with pronunciation hints and category-based progression.

Built with **Python (Flask)**, **SQLite**, **HTML/CSS**, and **JavaScript**.

---

## Features

- 📚 **500 Lithuanian words** organised by category and difficulty
- 👀 **Learn mode**
  - See the Lithuanian word
  - Reveal the English translation
  - View a beginner-friendly pronunciation hint
- ✍️ **Test mode**
  - Type the English translation
  - Get instant feedback
  - Score tracking (only in Test mode)
- 🗂️ Category selection (e.g. greetings, basics, food, verbs)
- 🧠 Progress stored locally in a database
- 🌿 Soft, calm, nature-inspired UI

---

## Tech Stack

**Backend**
- Python
- Flask
- SQLite

**Frontend**
- HTML
- CSS
- Vanilla JavaScript

**Data**
- `words.json` – source of truth for vocabulary and pronunciation

---

## Project Structure

lithuanian_app/
│
├── app.py # Flask application
├── import_words.py # Imports words.json into the database
├── migrate_add_pronunciation.py
├── migrate_add_unique_index.py
├── schema.sql # Database schema
├── words.json # 500-word Lithuanian dataset
├── requirements.txt
├── README.md
│
├── templates/
│ └── index.html
│
├── static/
│ ├── styles.css
│ └── app.js
│
└── app.db # Local database (NOT committed to Git)
