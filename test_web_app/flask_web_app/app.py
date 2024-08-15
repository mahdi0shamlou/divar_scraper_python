from flask import Flask, render_template, request
import sqlite3  # imported in core.main
from config import DATABASE
from core.main import *
app = Flask(__name__)


@app.route('/')
def index():
    query = request.args.get('query')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if query:
        cursor.execute('SELECT * FROM data_compeleted WHERE number LIKE ?', ('%' + query + '%',))
    else:
        cursor.execute('SELECT * FROM data_compeleted')
    posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT token FROM data_compeleted WHERE id = ?', (post_id,))
    post = cursor.fetchone()
    print(post)
    obj_serach = ShowData()
    post = obj_serach.Data_of_token(post[0])
    print(post)
    conn.close()
    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
