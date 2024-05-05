from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('database.db')

# Function to create the users table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Route to handle the login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Successful login, redirect to some page
            return redirect(url_for('dashboard'))
        else:
            # Login failed, show an error message
            return render_template('LoginPageFashion.html', error='Invalid username or password')
    
    # If it's a GET request, just render the login form
    return render_template('LoginPageFashion.html', error=None)

# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
