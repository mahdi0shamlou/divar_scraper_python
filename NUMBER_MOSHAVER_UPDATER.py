import pymysql
import sqlite3

# Connect to the MySQL database
mysql_connection = pymysql.connect(
    host='45.149.79.52',
    user='admin_arkafile',
    port=3306,
    password='eZtO7SOV',
    database='admin_arkafile_duplicate'
)

# Connect to the SQLite database
sqlite_connection = sqlite3.connect('posts.db')

try:
    with mysql_connection.cursor() as mysql_cursor, sqlite_connection as sqlite_conn:
        # Fetch data from the MySQL database
        mysql_cursor.execute("SELECT id, name, phone, type, creator_user_id, editor_user_id, created_at, updated_at FROM phonebooks")
        rows = mysql_cursor.fetchall()

        # Insert data into the SQLite database
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.executemany('''
            INSERT INTO moshaver_numbers (id, name, number, type, creator_id, editor_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', rows)

        sqlite_conn.commit()

        # Fetch relevant data from the MySQL users table
        mysql_cursor.execute("""
            SELECT 
                name, phone, 'consultant' AS type, creator_user_id, admin_user_id, created_at, updated_at 
            FROM users
        """)

        rows = mysql_cursor.fetchall()

        # Prepare the insert statement for the SQLite database
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.executemany('''
            INSERT INTO moshaver_numbers (
                name, number, type, creator_id, editor_id, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', rows)

        # Commit the changes to the SQLite database
        sqlite_conn.commit()


finally:
    mysql_connection.close()
    sqlite_connection.close()

print("Data transferred successfully.")
