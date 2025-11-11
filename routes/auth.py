from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login")
def login_page():
    """Página de login"""
    return render_template("login/login.html")

@auth_bp.route("/dashboard")
def dashboard():
    """Dashboard principal pós-login"""
    return render_template("dashboard/dashboard.html")