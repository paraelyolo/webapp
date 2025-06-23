from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
import json
import os

login_bp = Blueprint('login', __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, '..', 'users.json')

@login_bp.route('/')
def login():
    return render_template('login.html')

@login_bp.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    try:
        with open(USERS_FILE) as f:
            users = json.load(f)
    except Exception as e:
        return f"Error leyendo archivo de usuarios: {e}", 500

    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        session['user'] = username
        return redirect(url_for('dashboard.dashboard'))
    return "Login incorrecto", 401
