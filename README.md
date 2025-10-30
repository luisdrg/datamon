
---

# 🧠 Datamon — Flask + Supabase Math Game

A web version of the classic **Dataman** toy — built with **Flask**, **Python**, and **Supabase** for our Intro to CS final project.

---

## 🚀 Overview

Datamon lets you:

* Log in with Supabase
* Play math games (**Answer Checker**, **Memory Bank**, **Number Guesser**)
* Track your scores and review each question you answered

All math is **integer-only**, and division must use **quotient + remainder** (e.g. `10 ÷ 3 → 3 r 1`).

---

## ⚙️ Setup

```bash
git clone https://github.com/luisdrg/datamon.git
cd datamon
python -m venv venv
source venv/bin/activate     # or venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SECRET_KEY=some-flask-secret
```

Run:

```bash
flask run
```

Visit → [http://localhost:5000](http://localhost:5000)

---

## 🧱 Project Structure

```
datamon/
├── app.py                # Flask routes + main app
├── utils/
│   ├── core/             # Shared math + logic
│   ├── answer_checker.py # Complete game
│   ├── memory_bank.py    # Stub (next sprint)
│   ├── number_guesser.py # Stub (next sprint)
│   └── supabase_helpers.py
├── templates/            # HTML (Jinja)
└── static/css/style.css  # Styling
```

---

## 🧮 Database Schema (Supabase)

| Table                     | Used By        | Purpose                             |
| ------------------------- | -------------- | ----------------------------------- |
| `auth.users`              | Supabase       | User accounts                       |
| `scores`                  | All games      | Stores game session summaries       |
| `game_attempts`           | All games      | Stores every question + user answer |
| `memory_bank`             | Memory Bank    | Saved math problems                 |
| `number_guesser_attempts` | Number Guesser | User guess attempts                 |

### Diagram

```
users ──< scores ──< game_attempts
              ├──< memory_bank
              └──< number_guesser_attempts
```

---

### 🧾 Example SQL Schema

```sql
-- Shared scores table
create table if not exists scores (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users(id) on delete cascade,
  game text not null,
  correct int not null,
  total int not null,
  duration float,
  created_at timestamp default now()
);

-- Question-level detail for all games
create table if not exists game_attempts (
  id bigint generated always as identity primary key,
  score_id bigint references scores(id) on delete cascade,
  question text not null,
  user_answer text not null,
  correct_answer text not null,
  is_correct boolean not null,
  created_at timestamp default now()
);

-- Memory Bank problems
create table if not exists memory_bank (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users(id) on delete cascade,
  problem text not null,
  created_at timestamp default now()
);

-- Number Guesser results
create table if not exists number_guesser_attempts (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users(id) on delete cascade,
  tries int not null,
  secret_number int not null,
  created_at timestamp default now()
);
```

---

### 🧩 How Games Use Tables

| Game               | Writes To                                | Description                         |
| ------------------ | ---------------------------------------- | ----------------------------------- |
| **Answer Checker** | `scores`, `game_attempts`                | Saves each question + summary       |
| **Memory Bank**    | `memory_bank`, `scores`, `game_attempts` | Saves problems and practice results |
| **Number Guesser** | `number_guesser_attempts`, `scores`      | Saves tries and final result        |

---

## 🧠 Team Notes

* Keep logic in `/utils/`
* Reuse helpers in `/core/`
* Write clear commits:
* Test locally before pushing.

---
