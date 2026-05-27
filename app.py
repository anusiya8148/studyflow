import os
import sqlite3
import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

app = Flask(__name__)
app.secret_key = 'studyflow_secure_production_secret_key_192837465'
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                due_date TEXT,
                priority TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS journals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                mood TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS voice_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        conn.commit()

init_db()

MOTIVATIONAL_QUOTES = [
    "Believe in yourself. You are stronger than you think!",
    "Success is not final; failure is not fatal: It is the courage to continue that counts.",
    "The secret of getting ahead is getting started.",
    "Don't watch the clock; do what it does. Keep going.",
    "Your talent determines what you can do. Your motivation determines how much you are willing to do."
]

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')

        with get_db_connection() as conn:
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password security credentials.", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='scrypt')

        try:
            with get_db_connection() as conn:
                conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
                conn.commit()
            flash("Registration complete! Please log in below.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("An account using that email endpoint already exists.", "danger")
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    u_id = session['user_id']
    with get_db_connection() as conn:
        total_notes = conn.execute('SELECT COUNT(*) FROM notes WHERE user_id = ?', (u_id,)).fetchone()[0]
        total_tasks = conn.execute('SELECT COUNT(*) FROM tasks WHERE user_id = ?', (u_id,)).fetchone()[0]
        completed_tasks = conn.execute('SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = "Completed"', (u_id,)).fetchone()[0]

        recent_notes = conn.execute('SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC LIMIT 3', (u_id,)).fetchall()
        todo_tasks = conn.execute('SELECT * FROM tasks WHERE user_id = ? ORDER BY id DESC LIMIT 4', (u_id,)).fetchall()
        recent_journals = conn.execute('SELECT * FROM journals WHERE user_id = ? ORDER BY id DESC LIMIT 2', (u_id,)).fetchall()

    productivity = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0.0

    # Pre-calculated mathematically to eliminate inline template script linter crashes
    remaining_tasks = total_tasks - completed_tasks if total_tasks > completed_tasks else 0
    random_quote = random.choice(MOTIVATIONAL_QUOTES)

    return render_template('dashboard.html', total_notes=total_notes, total_tasks=total_tasks,
                           completed_tasks=completed_tasks, remaining_tasks=remaining_tasks,
                           productivity=productivity, recent_notes=recent_notes,
                           todo_tasks=todo_tasks, recent_journals=recent_journals, quote=random_quote)

@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    u_id = session['user_id']
    search = request.args.get('search', '').strip()
    with get_db_connection() as conn:
        if search:
            note_list = conn.execute('SELECT * FROM notes WHERE user_id = ? AND (title LIKE ? OR content LIKE ?) ORDER BY id DESC', (u_id, f'%{search}%', f'%{search}%')).fetchall()
        else:
            note_list = conn.execute('SELECT * FROM notes WHERE user_id = ? ORDER BY id DESC', (u_id,)).fetchall()

    if request.method == 'POST':
        title = request.form.get('title').strip()
        content = request.form.get('content').strip()
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with get_db_connection() as conn:
            conn.execute('INSERT INTO notes (user_id, title, content, created_at) VALUES (?, ?, ?, ?)', (u_id, title, content, now))
            conn.commit()
        flash('Note created successfully!', 'success')
        return redirect(url_for('notes'))

    return render_template('notes.html', notes=note_list, search=search)

@app.route('/notes/edit/<int:id>', methods=['POST'])
@login_required
def edit_note(id):
    u_id = session['user_id']
    title = request.form.get('title').strip()
    content = request.form.get('content').strip()
    with get_db_connection() as conn:
        conn.execute('UPDATE notes SET title = ?, content = ? WHERE id = ? AND user_id = ?', (title, content, id, u_id))
        conn.commit()
    flash('Note updated successfully.', 'success')
    return redirect(url_for('notes'))

@app.route('/notes/delete/<int:id>')
@login_required
def delete_note(id):
    u_id = session['user_id']
    with get_db_connection() as conn:
        conn.execute('DELETE FROM notes WHERE id = ? AND user_id = ?', (id, u_id))
        conn.commit()
    flash('Note deleted.', 'warning')
    return redirect(url_for('notes'))

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    u_id = session['user_id']
    if request.method == 'POST':
        title = request.form.get('title').strip()
        due_date = request.form.get('due_date')
        priority = request.form.get('priority')
        with get_db_connection() as conn:
            conn.execute('INSERT INTO tasks (user_id, title, due_date, priority) VALUES (?, ?, ?, ?)', (u_id, title, due_date, priority))
            conn.commit()
        flash('Task added successfully.', 'success')
        return redirect(url_for('tasks'))

    with get_db_connection() as conn:
        task_list = conn.execute('SELECT * FROM tasks WHERE user_id = ? ORDER BY id DESC', (u_id,)).fetchall()
    return render_template('tasks.html', tasks=task_list)

@app.route('/tasks/status/<int:id>/<string:status>')
@login_required
def change_task_status(id, status):
    u_id = session['user_id']
    target_status = 'Completed' if status == 'complete' else 'Pending'
    with get_db_connection() as conn:
        conn.execute('UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?', (target_status, id, u_id))
        conn.commit()
    flash(f'Task marked as {target_status}.', 'success')
    return redirect(request.referrer or url_for('tasks'))

@app.route('/tasks/edit/<int:id>', methods=['POST'])
@login_required
def edit_task(id):
    u_id = session['user_id']
    title = request.form.get('title').strip()
    due_date = request.form.get('due_date')
    priority = request.form.get('priority')
    with get_db_connection() as conn:
        conn.execute('UPDATE tasks SET title = ?, due_date = ?, priority = ? WHERE id = ? AND user_id = ?', (title, due_date, priority, id, u_id))
        conn.commit()
    flash('Task metadata modified.', 'success')
    return redirect(url_for('tasks'))

@app.route('/tasks/delete/<int:id>')
@login_required
def delete_task(id):
    u_id = session['user_id']
    with get_db_connection() as conn:
        conn.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (id, u_id))
        conn.commit()
    flash('Task removed.', 'warning')
    return redirect(url_for('tasks'))

@app.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    u_id = session['user_id']
    if request.method == 'POST':
        title = request.form.get('title').strip()
        content = request.form.get('content').strip()
        mood = request.form.get('mood', '😊')
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with get_db_connection() as conn:
            conn.execute('INSERT INTO journals (user_id, title, content, mood, created_at) VALUES (?, ?, ?, ?, ?)', (u_id, title, content, mood, now))
            conn.commit()
        flash('Journal entry recorded!', 'success')
        return redirect(url_for('journal'))

    with get_db_connection() as conn:
        entries = conn.execute('SELECT * FROM journals WHERE user_id = ? ORDER BY id DESC', (u_id,)).fetchall()
    return render_template('journal.html', journals=entries)

@app.route('/journal/edit/<int:id>', methods=['POST'])
@login_required
def edit_journal(id):
    u_id = session['user_id']
    title = request.form.get('title').strip()
    content = request.form.get('content').strip()
    mood = request.form.get('mood')
    with get_db_connection() as conn:
        conn.execute('UPDATE journals SET title = ?, content = ?, mood = ? WHERE id = ? AND user_id = ?', (title, content, mood, id, u_id))
        conn.commit()
    flash('Journal entry updated.', 'success')
    return redirect(url_for('journal'))

@app.route('/journal/delete/<int:id>')
@login_required
def delete_journal(id):
    u_id = session['user_id']
    with get_db_connection() as conn:
        conn.execute('DELETE FROM journals WHERE id = ? AND user_id = ?', (id, u_id))
        conn.commit()
    flash('Journal log dropped.', 'warning')
    return redirect(url_for('journal'))

@app.route('/voice', methods=['GET', 'POST'])
@login_required
def voice():
    u_id = session['user_id']
    if request.method == 'POST':
        if 'audio_data' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        file = request.files['audio_data']
        title = request.form.get('title', f"Voice Note ({datetime.now().strftime('%Y-%m-%d')})").strip()
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Empty filename'}), 400

        filename = f"voice_{u_id}_{int(datetime.now().timestamp())}.webm"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        with get_db_connection() as conn:
            conn.execute('INSERT INTO voice_notes (user_id, filename, title, created_at) VALUES (?, ?, ?, ?)', (u_id, filename, title, now))
            conn.commit()
        return jsonify({'success': True})

    with get_db_connection() as conn:
        v_list = conn.execute('SELECT * FROM voice_notes WHERE user_id = ? ORDER BY id DESC', (u_id,)).fetchall()
    return render_template('voice.html', voice_notes=v_list)

@app.route('/voice/delete/<int:id>')
@login_required
def delete_voice(id):
    u_id = session['user_id']
    with get_db_connection() as conn:
        row = conn.execute('SELECT * FROM voice_notes WHERE id = ? AND user_id = ?', (id, u_id)).fetchone()
        if row:
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], row['filename']))
            except FileNotFoundError:
                pass
            conn.execute('DELETE FROM voice_notes WHERE id = ? AND user_id = ?', (id, u_id))
            conn.commit()
    flash('Voice artifact deleted.', 'warning')
    return redirect(url_for('voice'))

@app.route('/motivation')
@login_required
def motivation():
    return render_template('motivation.html', quote=random.choice(MOTIVATIONAL_QUOTES), all_quotes=MOTIVATIONAL_QUOTES)

@app.route('/api/quote')
def get_quote():
    return jsonify({'quote': random.choice(MOTIVATIONAL_QUOTES)})

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/logout/confirm')
def logout_confirm():
    session.clear()
    flash("Session terminated successfully.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)