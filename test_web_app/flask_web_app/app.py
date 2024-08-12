from flask import Flask, render_template, request
import sqlite3
from models import init_db
from config import DATABASE

app = Flask(__name__)

# Initialize the database
init_db()

@app.route('/')
def index():
    query = request.args.get('query')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if query:
        cursor.execute('SELECT * FROM personal_number WHERE number LIKE ?', ('%' + query + '%',))
    else:
        cursor.execute('SELECT * FROM personal_number')
    posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM personal_number WHERE id = ?', (post_id,))
    post = cursor.fetchone()
    conn.close()
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
