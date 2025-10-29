from flask import Flask, render_template, request, redirect, url_for, session
from config import SECRET_KEY, supabase
from utils.games import check_answer
from utils.supabase_helpers import register_user, login_user, save_score

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
        email = request.form['email']
        password = request.form['password']
        try:
            res = register_user(email, password)
            # If no error raised, go to login
            return redirect(url_for('login'))
        except Exception as e:
            error = "Registration failed. " + str(e)
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
                session['user'] = {'id': res.user.id, 'email': res.user.email}
                # Reset counters on fresh login
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
        is_correct, correct_display = check_answer(problem, user_answer)

        # Keep score: after each submission, count increments; 10 attempts per round
        session['score'] = session.get('score', 0)
        session['count'] = session.get('count', 0) + 1

        if is_correct:
            session['score'] += 1
            feedback = "✅ Correct!"
        else:
            feedback = f"❌ EEE! Correct answer was {correct_display}"

        # After 10 problems, save and show summary
        if session['count'] >= 10:
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

if __name__ == '__main__':
    app.run(debug=True)
