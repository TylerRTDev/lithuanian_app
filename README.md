# Lithuanian Flashcard Learning App 🇱🇹🌿

A simple, beginner-friendly language learning web app inspired by flashcards.  
The app helps users learn Lithuanian vocabulary through **Learn** and **Test** modes, with pronunciation hints and category-based progression.

Built with **Python (Flask)**, **SQLite**, **HTML/CSS**, and **JavaScript**.

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
## Running the App (Windows – PowerShell)

Activate virtual environment:
.\.venv\Scripts\Activate.ps1

Run the app:
python app.py

Screenshots:
<img width="773" height="382" alt="image" src="https://github.com/user-attachments/assets/922e6bf4-5d63-4e48-b8dd-f43743226c1b" />
<img width="768" height="465" alt="image" src="https://github.com/user-attachments/assets/05b62cad-3229-4a92-bc14-95b6d7c364c2" />
<img width="226" height="377" alt="image" src="https://github.com/user-attachments/assets/f9f81026-c9a1-431a-8b0a-afff4fc566bb" />
<img width="763" height="385" alt="image" src="https://github.com/user-attachments/assets/9bee7e82-a327-412e-a70d-11216c182d59" />



