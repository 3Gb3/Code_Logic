from flask import Blueprint, render_template, redirect, url_for

aulas_bp = Blueprint('aulas', __name__, url_prefix='/aulas')

# Referência para o banco de dados Firestore
db = None

def set_firestore_client(firestore_client):
    """Define o cliente Firestore para as rotas de aulas"""
    global db
    db = firestore_client

@aulas_bp.route("/")
def aulas_index():
    """Redireciona para dashboard"""
    return redirect(url_for('dashboard'))

# Rotas dos módulos
@aulas_bp.route("/sequencial")
def sequencial():
    """Lobby do módulo Programação Sequencial"""
    return render_template("aulas/sequencial.html")

@aulas_bp.route("/comparativa")
def comparativa():
    """Lobby do módulo Estruturas Comparativas"""
    # Verificação será feita via JavaScript no template
    return render_template("aulas/comparativa.html")

@aulas_bp.route("/repetitiva")
def repetitiva():
    """Lobby do módulo Estruturas Repetitivas"""
    # Verificação será feita via JavaScript no template
    return render_template("aulas/repetitiva.html")

@aulas_bp.route("/vetores")
def vetores():
    """Lobby do módulo Vetores"""
    # Verificação será feita via JavaScript no template
    return render_template("aulas/vetores.html")

@aulas_bp.route("/matrizes")
def matrizes():
    """Lobby do módulo Matrizes"""
    # Verificação será feita via JavaScript no template
    return render_template("aulas/matrizes.html")