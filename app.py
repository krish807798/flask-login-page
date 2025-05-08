from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
app.secret_key = 'Kribhai'

# Dummy user for authentication
users = {
    "krish": generate_password_hash("pas1"),
}

# Predefined secret key for registration (Can be changed to any key)
SECRET_KEY = "krishwillfuckyouhaters"

# In-memory note storage (session-based)
@app.before_request
def load_notes():
    if 'notes' not in session:
        session['notes'] = []  # Initialize the notes list if not present
    
    # Ensure session['last_activity'] is timezone naive
    if 'last_activity' in session:
        # If it's a timezone-aware datetime, make it naive (ignoring timezone)
        if session['last_activity'].tzinfo is not None:
            session['last_activity'] = session['last_activity'].replace(tzinfo=None)

        # Check for session expiry using naive datetime
        if datetime.now() - session['last_activity'] > timedelta(minutes=30):
            session.pop('username', None)
            flash("Session expired. Please log in again.")
            return redirect(url_for('login'))
    
    # Update last activity to the current naive datetime
    session['last_activity'] = datetime.now()

# Setup logging configuration
logging.basicConfig(filename="user_activity.log", level=logging.INFO, 
                    format="%(asctime)s - %(message)s")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            # Log the successful login attempt
            logging.info(f"User '{username}' logged in.")
            return redirect(url_for('welcome'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('welcome'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        secret_key = request.form['secret_key']

        # Check if the secret key is correct
        if secret_key != SECRET_KEY:
            flash("Invalid secret key. You cannot register.")
            return redirect(url_for('register'))

        # Check if the username already exists
        if username in users:
            flash("Username already exists.")
            return redirect(url_for('register'))

        # Create a new user with hashed password
        users[username] = generate_password_hash(password)
        # Log the registration attempt
        logging.info(f"New user '{username}' registered.")
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('welcome.html')

@app.route('/calculator')
def calculator():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('calculator.html')

@app.route('/tictaktoe')
def tictaktoe():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('tictaktoe.html')

@app.route('/flappybird')
def flappybird():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('flappybird.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes_app():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Handling POST requests (adding notes)
    if request.method == 'POST':
        content = request.form.get('note')
        if content:
            session['notes'].append(content)  # Add note to the session
            flash("Note added successfully.")
            session.modified = True  # Mark the session as modified so it gets updated

        return redirect(url_for('notes_app'))

    # Rendering the notes page
    return render_template('notes.html', notes=session['notes'])

@app.route('/delete_note/<int:index>', methods=['POST'])
def delete_note(index):
    if 'username' not in session:
        return redirect(url_for('login'))

    if 0 <= index < len(session['notes']):
        del session['notes'][index]  # Remove the note from the session
        flash("Note deleted.")
        session.modified = True  # Mark the session as modified so it gets updated
    return redirect(url_for('notes_app'))

@app.route('/logout')
def logout():
    if 'username' in session:
        logging.info(f"User '{session['username']}' logged out.")
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/activity_log')
def activity_log():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Read the log file and display the contents
    with open("user_activity.log", "r") as log_file:
        log_data = log_file.readlines()

    return render_template('activity_log.html', log_data=log_data)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
