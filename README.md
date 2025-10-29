# Dataman: Answer Checker (Flask + Supabase)

A minimal web remake of the classic Dataman "Answer Checker".
- Users enter **their own math problem** and an **answer guess**.
- App checks correctness, gives "✅ Correct!" or "❌ EEE!"
- After 10 problems, the score is saved to Supabase.

## 1) Setup

```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
# venv\Scripts\activate      # Windows

pip install -r requirements.txt
cp .env.example .env           # then edit .env with your Supabase creds
```

In Supabase SQL editor, run:

```sql
create table if not exists scores (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users(id) on delete cascade,
  game text,
  score int,
  created_at timestamp default now()
);
```

## 2) Run

```bash
flask --app app run --debug
```

Visit http://127.0.0.1:5000

## 3) Notes

- No fancy JS; plain Flask forms.
- Accepts operators: +, -, *, x, ×, /, ÷
- Division answers: you can enter either a decimal **or** `Q r R` remainder format, e.g. `7 r 1`.
- The correct answer display will show remainder format when appropriate.
