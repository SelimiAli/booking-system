from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv
import mysql.connector
import os

# Til at .env filen
load.dotenv()

# Initialiserer Flask applikationen med statiske filer
app = Flask(__name__, static_url_path='/static')
# Genererer en hemmelig nøgle til sessioner
app.secret_key = os.urandom(24)

# Konfigurerer databaseforbindelsen til MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Alarm123.",
    database="booking_db"
)
# Opretter en cursor til at udføre SQL-forespørgsler
cursor = db.cursor(dictionary=True)

# Decorator funktion til at kontrollere om brugeren er logget ind
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Tjekker om bruger-id findes i sessionen
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route til login-siden
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Håndterer login-formular
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Søger efter brugeren i databasen
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        # Verificerer brugerens legitimationsoplysninger
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash('Ugyldigt brugernavn eller adgangskode')
    return render_template('login.html')

# Route til registreringssiden
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Håndterer registreringsformular
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Krypterer adgangskoden før den gemmes
        hashed_password = generate_password_hash(password)
        
        try:
            # Forsøger at oprette ny bruger
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                         (username, hashed_password))
            db.commit()
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            # Håndterer hvis brugernavnet allerede eksisterer
            flash('Brugernavn findes allerede')
    return render_template('register.html')

# Route til at logge ud
@app.route('/logout')
def logout():
    # Rydder sessionen og logger brugeren ud
    session.clear()
    return redirect(url_for('login'))

# Hovedsiden - kræver login
@app.route('/')
@login_required
def home():
    # Henter alle bookinger fra databasen
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    return render_template('index.html', bookings=bookings)

# Route til at oprette en ny booking
@app.route('/book', methods=['POST'])
@login_required
def book():
    # Henter data fra bookingformularen
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']
    
    # Indsætter ny booking i databasen
    sql = "INSERT INTO bookings (name, date, time, user_id) VALUES (%s, %s, %s, %s)"
    values = (name, date, time, session['user_id'])
    cursor.execute(sql, values)
    db.commit()
    
    return redirect('/')

# Route til at slette en booking
@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    # Sletter den valgte booking
    sql = "DELETE FROM bookings WHERE id = %s AND user_id = %s"
    values = (id, session['user_id'])
    cursor.execute(sql, values)
    db.commit()
    return redirect('/')

# Route til at opdatere en booking
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        # Opdaterer eksisterende booking
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        
        sql = "UPDATE bookings SET name = %s, date = %s, time = %s WHERE id = %s AND user_id = %s"
        values = (name, date, time, id, session['user_id'])
        cursor.execute(sql, values)
        db.commit()
        return redirect('/')
    else:
        # Viser opdateringsformular med eksisterende data
        cursor.execute("SELECT * FROM bookings WHERE id = %s AND user_id = %s", 
                      (id, session['user_id']))
        booking = cursor.fetchone()
        return render_template('update.html', booking=booking)

# Starter applikationen i debug-tilstand
if __name__ == '__main__':
    app.run(debug=True)
