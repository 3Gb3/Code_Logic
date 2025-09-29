from flask import Blueprint, render_template, abort

exercicios_bp = Blueprint('exercicios', __name__, url_prefix='/exercicios')

# === ROTAS SEQUENCIAL ===
@exercicios_bp.route("/sequencial/aula/<int:aula_num>")
def exercicio_sequencial(aula_num):
    """Exercícios do módulo Sequencial"""
    if 1 <= aula_num <= 10:
        template_path = f"exercicios/sequencial/aula{aula_num}.html"
        try:
            return render_template(template_path)
        except:
            return render_template("exercicios/template_generico.html", 
                                 modulo="Sequencial", aula_num=aula_num)
    else:
        abort(404)

# === ROTAS COMPARATIVA ===
@exercicios_bp.route("/comparativa/aula/<int:aula_num>")
def exercicio_comparativa(aula_num):
    """Exercícios do módulo Estruturas Comparativas"""
    if 1 <= aula_num <= 10:
        template_path = f"exercicios/comparativa/aula{aula_num}.html"
        try:
            return render_template(template_path)
        except:
            return render_template("exercicios/template_generico.html", 
                                 modulo="Comparativa", aula_num=aula_num)
    else:
        abort(404)

# === ROTAS REPETITIVA ===
@exercicios_bp.route("/repetitiva/aula/<int:aula_num>")
def exercicio_repetitiva(aula_num):
    """Exercícios do módulo Estruturas Repetitivas"""
    if 1 <= aula_num <= 10:
        template_path = f"exercicios/repetitiva/aula{aula_num}.html"
        try:
            return render_template(template_path)
        except:
            return render_template("exercicios/template_generico.html", 
                                 modulo="Repetitiva", aula_num=aula_num)
    else:
        abort(404)

# === ROTAS VETORES ===
@exercicios_bp.route("/vetores/aula/<int:aula_num>")
def exercicio_vetores(aula_num):
    """Exercícios do módulo Vetores"""
    if 1 <= aula_num <= 10:
        template_path = f"exercicios/vetores/aula{aula_num}.html"
        try:
            return render_template(template_path)
        except:
            return render_template("exercicios/template_generico.html", 
                                 modulo="Vetores", aula_num=aula_num)
    else:
        abort(404)

# === ROTAS MATRIZES ===
@exercicios_bp.route("/matrizes/aula/<int:aula_num>")
def exercicio_matrizes(aula_num):
    """Exercícios do módulo Matrizes"""
    if 1 <= aula_num <= 10:
        template_path = f"exercicios/matrizes/aula{aula_num}.html"
        try:
            return render_template(template_path)
        except:
            return render_template("exercicios/template_generico.html", 
                                 modulo="Matrizes", aula_num=aula_num)
    else:
        abort(404)