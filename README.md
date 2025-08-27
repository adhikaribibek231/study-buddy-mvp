
# Study Buddy MVP

**Study Buddy MVP** is an AI-powered study assistant designed to help students learn more efficiently. This minimal viable product (MVP) allows users to transform their lecture notes or study materials into concise summaries and interactive flashcards, while using a simple spaced-repetition system to optimize review schedules.

With Study Buddy MVP, students can focus on **learning**, not manual note-taking or flashcard creation.

---

## Features

* **Upload Lecture Notes:** Supports PDF and TXT files.
* **AI-Powered Summarization:** Automatically generates short, easy-to-read summaries of your notes.
* **Flashcard Generation:** Converts key points into Q\&A flashcards for active recall.
* **Spaced Repetition:** Simple review schedule to maximize memory retention.
* **Web Interface:** Basic Django-based UI for uploading notes, viewing summaries, and reviewing flashcards.

---

## Tech Stack

* **Backend:** Python, Django
* **AI Models:** Hugging Face Transformers (`t5-small`, `distilbart-cnn-12-6`)
* **Database:** SQLite
* **Frontend:** Django Templates + Bootstrap/Tailwind (basic UI)

---

## How It Works

1. **Upload notes** (PDF or TXT).
2. **Summarization**: AI generates a concise summary.
3. **Flashcard creation**: Key points are turned into Q\&A style flashcards.
4. **Review loop**: Spaced repetition algorithm schedules flashcard reviews.

---

## Getting Started

1. Clone the repository:

   ```bash
   git clone <repo_url>
   cd studybuddy
   ```
2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```
3. Run migrations and start the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
4. Open `http://127.0.0.1:8000` in your browser.

---

## Future Plans

* Add **user accounts and progress tracking**.
* Support **multimedia flashcards** (images/audio).
* Smarter AI recommendations for **which flashcards to review next**.
* Offline functionality for areas with limited internet.

---
