from flask import Flask, render_template, request, redirect, url_for, session
from config import SECRET_KEY, supabase
from utils.answer_checker import play_answer_checker
from utils.supabase_helpers import register_user, login_user, save_score

# Constants
ANSWER_CHECKER_TOTAL_PROBLEMS = 10

app = Flask(__name__)
app.secret_key = SECRET_KEY

# ---------- Auth & Home ----------
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            error = "Passwords do not match."
        else:
            try:
                res = register_user(email, password, name)
                if res.user:
                    return redirect(url_for('login'))
                else:
                    error = "Registration failed. Try again."
            except Exception as e:
                error = f"Registration failed: {e}"

    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            res = login_user(email, password)
            if res and res.user:
                session['user'] = {
                    'id': res.user.id,
                    'email': res.user.email,
                    'name': res.user.user_metadata.get('name') if res.user.user_metadata else None
                }
                session['score'] = 0
                session['count'] = 0
                return redirect(url_for('index'))
            else:
                error = "Login failed."
        except Exception as e:
            error = "Login failed. " + str(e)
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('score', None)
    session.pop('count', None)
    return redirect(url_for('login'))

# ---------- Answer Checker ----------
@app.route('/answer_checker', methods=['GET', 'POST'])
def answer_checker():
    if 'user' not in session:
        return redirect(url_for('login'))

    feedback = None
    problem_prefill = request.form.get('problem', '') if request.method == 'POST' else ''
    user_answer_prefill = ''

    if request.method == 'POST':
        problem = request.form['problem']
        user_answer = request.form['user_answer']
        is_correct, correct_display = play_answer_checker(problem, user_answer)

        # Keep score: after each submission, count increments; 10 attempts per round
        session['score'] = session.get('score', 0)
        session['count'] = session.get('count', 0) + 1

        if is_correct:
            session['score'] += 1
            feedback = "✅ Correct!"
        else:
            feedback = f"❌ EEE! Correct answer was {correct_display}"

        # After 10 problems, save and show summary
        if session['count'] >= ANSWER_CHECKER_TOTAL_PROBLEMS:
            if 'user' in session and session['user'].get('id'):
                try:
                    save_score(session['user']['id'], session['score'])
                except Exception as e:
                    print('[WARN] Could not save score:', e)

            final_score = session['score']
            # Reset for next round
            session['score'] = 0
            session['count'] = 0
            return render_template('answer_checker.html', done=True, score=final_score)

        # Keep last problem in the input for convenience
        problem_prefill = problem
        user_answer_prefill = ''

    return render_template('answer_checker.html',
                           feedback=feedback,
                           problem_prefill=problem_prefill,
                           user_answer_prefill=user_answer_prefill,
                           score=session.get('score', 0),
                           count=session.get('count', 0))

# ---------- Memory Bank ----------
@app.route('/memory_bank', methods=['GET', 'POST'])
def memory_bank():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Stub: just a placeholder page for now
    return render_template('memory_bank.html')


# ---------- Number Guesser ----------
@app.route('/number_guesser', methods=['GET', 'POST'])
def number_guesser():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Stub: placeholder
    return render_template('number_guesser.html')


if __name__ == '__main__':
    app.run(debug=True)
