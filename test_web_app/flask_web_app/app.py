from flask import Flask, render_template, request, jsonify
import sqlite3
from config import DATABASE
from core.main import ShowData
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log')


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    query = request.args.get('query')
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if query:
                cursor.execute('SELECT * FROM data_compeleted WHERE number LIKE ?', ('%' + query + '%',))
            else:
                cursor.execute('SELECT * FROM data_compeleted')
            posts = cursor.fetchall()
        return render_template('index.html', posts=posts)
    except sqlite3.Error as e:
        logging.error(f'Database error: {e}')
        return jsonify({"error": "Database error"}), 500


@app.route('/post/<int:post_id>')
def post(post_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT token FROM data_compeleted WHERE id = ?', (post_id,))
            post = cursor.fetchone()
            if post:
                obj_serach = ShowData()
                post = obj_serach.Data_of_token(post['token'])
                return render_template('post.html', post=post)
            else:
                return jsonify({"error": "Post not found"}), 404
    except sqlite3.Error as e:
        logging.error(f'Database error: {e}')
        return jsonify({"error": "Database error"}), 500


# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# Error handler for 404 Not Found Error
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
