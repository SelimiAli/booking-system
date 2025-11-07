from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import mysql.connector
import os
from config import DB_CONFIG, SECRET_KEY

# Initialiserer Flask applikationen med statiske filer
app = Flask(__name__, static_url_path='/static')
# Bruger hemmelig nøgle fra config
app.secret_key = SECRET_KEY

# Konfigurerer databaseforbindelsen til MySQL fra config
db = mysql.connector.connect(**DB_CONFIG)
# Opretter en cursor til at udføre SQL-forespørgsler
cursor = db.cursor(dictionary=True)

# Resten af din eksisterende kode...