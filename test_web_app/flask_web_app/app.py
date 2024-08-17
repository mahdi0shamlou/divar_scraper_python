from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import requests
import sqlite3
from config import DATABASE
from core.main import ShowData
import logging
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log')

# Path to CSV file
CSV_FILE_PATH = '../../Files/WORD_list_check.csv'  # Update this path to your CSV file
UPLOAD_FOLDER = '../../Files/'  # Folder to save uploaded CSV files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


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
                cursor.execute('SELECT * FROM personal_number WHERE number LIKE ?', ('%' + query + '%',))
            else:
                cursor.execute('SELECT * FROM personal_number')
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
            cursor.execute('SELECT token FROM personal_number WHERE id = ?', (post_id,))
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


# Route to view and edit tokens_divar table
@app.route('/tokens_divar', methods=['GET', 'POST'])
def tokens_divar():
    try:
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'add':
                jwt_token_divar = request.form['jwt_token_divar']
                number = request.form['number']
                # Insert new data into the table
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO tokens_divar (jwt_token_divar, number) VALUES (?, ?)', (jwt_token_divar, number))
                    conn.commit()
            elif action == 'delete':
                token_id = request.form['id']
                # Delete data from the table
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM tokens_divar WHERE id = ?', (token_id,))
                    conn.commit()
            elif action == 'update_jwt':
                token_id = request.form['id']
                new_jwt_token_divar = request.form['new_jwt_token_divar']
                # Update jwt_token_divar in the table
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE tokens_divar SET jwt_token_divar = ? WHERE id = ?', (new_jwt_token_divar, token_id))
                    conn.commit()
            elif action == 'update_number':
                token_id = request.form['id']
                new_number = request.form['new_number']
                # Update number in the table
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE tokens_divar SET number = ? WHERE id = ?', (new_number, token_id))
                    conn.commit()

            return redirect(url_for('tokens_divar'))

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tokens_divar')
            tokens = cursor.fetchall()
        return render_template('tokens_divar.html', tokens=tokens)

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


@app.route('/view_csv')
def view_csv():
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        return render_template('view_csv.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
    except Exception as e:
        logging.error(f'Error reading CSV file: {e}')
        return jsonify({"error": "Error reading CSV file"}), 500


@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    try:
        if request.method == 'POST':
            # Check if the file part exists in the request
            if 'file' not in request.files:
                return jsonify({"error": "No file part in the request"}), 400

            file = request.files['file']

            # If the user does not select a file, the browser submits an empty file without a filename
            if file.filename == '':
                return jsonify({"error": "No selected file"}), 400

            if file and allowed_file(file.filename):
                # Save the new CSV file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'WORD_list_check.csv')
                file.save(file_path)

                # Optionally, validate the new CSV file contents here

                return redirect(url_for('view_csv'))

        return render_template('upload_csv.html')

    except Exception as e:
        logging.error(f'Error uploading CSV file: {e}')
        return jsonify({"error": "Error uploading CSV file"}), 500


@app.route('/get_jwt_token', methods=['GET', 'POST'])
def get_jwt_token():
    response_data = {}
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        code = request.form.get('code')
        action_type = request.form.get('action_type')

        if phone_number and action_type == 'authenticate':
            url = 'https://api.divar.ir/v5/auth/authenticate'
            headers = {
                'Content-Type': 'application/json'
            }
            payload = {
                'phone': phone_number
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                flash('Authentication request successful: {}'.format(response_data), 'success')
            else:
                flash('Failed to authenticate. Status code: {}'.format(response.status_code), 'danger')
        elif phone_number and code and action_type == 'confirm':
            url = 'https://api.divar.ir/v5/auth/confirm'
            headers = {
                'Content-Type': 'application/json'
            }
            payload = {
                'phone': phone_number,
                'code': code
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                flash('Confirmation request successful: {}'.format(response_data), 'success')
            else:
                flash('Failed to confirm. Status code: {}'.format(response.status_code), 'danger')
        else:
            flash('Please enter all required fields correctly.', 'warning')

        return render_template('get_jwt_token.html', response_data=response_data)

    return render_template('get_jwt_token.html', response_data=response_data)


@app.route('/control_table', methods=['GET', 'POST'])
def control_table():
    if request.method == 'POST':
        action = request.form.get('action')
        row_id = request.form.get('row_id')
        print(row_id)
        print(action)
        if action and row_id:
            flash(f'{action.capitalize()} action triggered for row {row_id}', 'success')
        else:
            flash('Invalid action or row ID', 'danger')
        return redirect(url_for('control_table'))

    return render_template('control_table.html')


# Ensure you have other routes and your run configuration

if __name__ == '__main__':
    app.run(debug=True)
