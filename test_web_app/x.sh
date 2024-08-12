#!/bin/bash

PROJECT_DIR="flask_web_app"

# Create project directory
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Create directories
mkdir -p templates static

# Create app.py
cat <<EOL > app.py
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
        cursor.execute('SELECT * FROM posts WHERE title LIKE ?', ('%' + query + '%',))
    else:
        cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = cursor.fetchone()
    conn.close()
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
EOL

# Create database.py
cat <<EOL > database.py
import sqlite3
from config import DATABASE

def connect_db():
    return sqlite3.connect(DATABASE)
EOL

# Create models.py
cat <<EOL > models.py
import sqlite3
from config import DATABASE

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT
                      )''')
    conn.commit()
    conn.close()
EOL

# Create config.py
cat <<EOL > config.py
DATABASE = 'posts.db'
EOL

# Create templates/base.html
cat <<EOL > templates/base.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Web App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <header>
        <h1>Flask Web App</h1>
        <form id="search-form" action="{{ url_for('index') }}" method="GET">
            <input type="text" name="query" placeholder="Search posts..." value="{{ request.args.get('query', '') }}">
            <button type="submit">Search</button>
        </form>
    </header>
    <div id="loader" class="loader">
        <img src="{{ url_for('static', filename='loader.gif') }}" alt="Loading...">
    </div>
    <main id="content">
        {% block content %}{% endblock %}
    </main>
    <footer>
        <p>&copy; 2024 Flask Web App</p>
    </footer>
    <script>
        document.getElementById('search-form').onsubmit = function() {
            document.getElementById('loader').style.display = 'block';
            document.getElementById('content').style.display = 'none';
            return true;
        };
    </script>
</body>
</html>
EOL

# Create templates/index.html
cat <<EOL > templates/index.html
{% extends 'base.html' %}

{% block content %}
<h2>Posts</h2>
<table>
    <thead>
        <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Content</th>
        </tr>
    </thead>
    <tbody>
        {% for post in posts %}
        <tr>
            <td>{{ post[0] }}</td>
            <td><a href="{{ url_for('post', post_id=post[0]) }}">{{ post[1] }}</a></td>
            <td>{{ post[2] }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
EOL

# Create templates/post.html
cat <<EOL > templates/post.html
{% extends 'base.html' %}

{% block content %}
<h2>{{ post[1] }}</h2>
<p>{{ post[2] }}</p>
{% endblock %}
EOL

# Create static/styles.css
cat <<EOL > static/styles.css
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background: #f4f4f4;
    color: #333;
}

header {
    background: #333;
    color: #fff;
    padding: 1rem;
    text-align: center;
    position: sticky;
    top: 0;
}

header h1 {
    margin: 0;
}

header form {
    margin-top: 1rem;
}

header input[type="text"] {
    padding: 0.5rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
}

header button {
    padding: 0.5rem;
    font-size: 1rem;
    border: none;
    background: #0066cc;
    color: white;
    border-radius: 5px;
    cursor: pointer;
}

header button:hover {
    background: #004d99;
}

main {
    flex: 1;
    padding: 1rem;
}

footer {
    background: #333;
    color: #fff;
    text-align: center;
    padding: 1rem;
}

h2 {
    color: #333;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
}

table th, table td {
    border: 1px solid #ccc;
    padding: 0.5rem;
    text-align: left;
}

table th {
    background: #f2f2f2;
}

table tr:nth-child(even) {
    background: #f9f9f9;
}

#loader {
    display: none;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.loader img {
    width: 50px;
    height: 50px;
}
EOL

# Download a sample loader.gif if not exist
if [ ! -f static/loader.gif ]; then
  curl -o static/loader.gif https://i.gifer.com/YCZH.gif
fi

echo "Project structure and files created successfully."

