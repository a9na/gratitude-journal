from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('gratitude.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS entries
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT,
                      content TEXT)''')
        conn.commit()

init_db()

@app.route('/')
def index():
    with sqlite3.connect('gratitude.db') as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM entries ORDER BY date DESC')
        entries = c.fetchall()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    content = request.form['content']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect('gratitude.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO entries (date, content) VALUES (?, ?)', (date, content))
        conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
