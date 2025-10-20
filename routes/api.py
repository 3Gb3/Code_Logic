from flask import Blueprint, request, jsonify
from firebase_admin import auth, firestore
import logging

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Referência para o banco de dados Firestore (será injetada pelo app principal)
db = None

def set_firestore_client(firestore_client):
    """Define o cliente Firestore para as rotas da API"""
    global db
    db = firestore_client

def verify_token_with_tolerance(token, max_retries=3):
    """Verifica token Firebase com tolerância para clock skew"""
    for attempt in range(max_retries):
        try:
            # Aumenta a tolerância a cada tentativa
            clock_skew = 30 + (attempt * 30)  # 30s, 60s, 90s
            decoded_token = auth.verify_id_token(token, check_revoked=False, clock_skew_seconds=clock_skew)
            return decoded_token
        except auth.InvalidIdTokenError as e:
            if "Token used too early" in str(e) and attempt < max_retries - 1:
                logging.warning(f"Clock skew detectado, tentativa {attempt + 1}/{max_retries}")
                import time
                time.sleep(0.5)
                continue
            else:
                raise e
        except Exception as e:
            if attempt < max_retries - 1:
                logging.warning(f"Erro na verificação do token, tentativa {attempt + 1}/{max_retries}: {e}")
                import time
                time.sleep(0.5)
                continue
            else:
                raise e
    
    raise Exception("Falha na verificação do token após múltiplas tentativas")

@api_bp.route("/verify-auth", methods=["POST"])
def verify_auth():
    """Verifica autenticação via token ID"""
    try:
        data = request.json
        if not data or 'idToken' not in data:
            return jsonify({"error": "Token ID não fornecido"}), 400
        
        # Verifica o token ID
        decoded_token = auth.verify_id_token(data['idToken'])
        user_uid = decoded_token['uid']
        user_email = decoded_token.get('email', 'Usuário')
        
        return jsonify({
            "success": True,
            "uid": user_uid,
            "email": user_email,
            "message": "Usuário autenticado com sucesso"
        })
        
    except Exception as e:
        logging.error(f"Erro na verificação de autenticação: {e}")
        return jsonify({"error": f"Falha na autenticação: {str(e)}"}), 401

@api_bp.route("/protegido", methods=["GET"])
def protegido():
    """Rota protegida de exemplo"""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Token ausente"}), 401
    try:
        decoded_token = verify_token_with_tolerance(token)
        return jsonify({"ok": True, "uid": decoded_token["uid"], "email": decoded_token.get("email")})
    except Exception as e:
        logging.error(f"Erro ao verificar token: {e}")
        return jsonify({"error": "Token inválido ou expirado"}), 401

@api_bp.route("/execute", methods=["POST"])
def execute_code():
    """API para execução de código Python"""
    try:
        from utils.executor import executor
        
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({"error": "Código não fornecido"}), 400
        
        code = data['code']
        
        # Valida sintaxe primeiro
        validation = executor.validate_code(code)
        if not validation['valid']:
            return jsonify({
                "success": False,
                "output": "",
                "error": validation['error']
            })
        
        # Executa o código
        result = executor.execute_python_code(code)
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Erro na execução: {e}")
        return jsonify({
            "success": False,
            "output": "",
            "error": "Erro interno do servidor"
        }), 500

@api_bp.route("/correct", methods=["POST"])
def correct_exercise():
    """API para correção automática de exercícios"""
    try:
        # Importa as dependências
        try:
            from utils.executor import executor
            from utils.ai_corrector import corrector
        except ImportError as ie:
            logging.error(f"Erro ao importar módulos: {ie}")
            return jsonify({
                "success": False,
                "error": "Erro ao carregar módulos de correção",
                "details": str(ie)
            }), 500
        
        # Obtém dados da requisição
        data = request.get_json()
        logging.info(f"Dados recebidos: {data}")
        
        if not data or 'code' not in data or 'exercise_description' not in data:
            logging.warning("Dados incompletos na requisição")
            return jsonify({
                "success": False,
                "error": "Dados incompletos. É necessário enviar 'code' e 'exercise_description'."
            }), 400
        
        code = data['code']
        exercise_description = data['exercise_description']
        lesson_number = data.get('lesson_number', 1)
        
        logging.info(f"Validando código da aula {lesson_number}")
        
        # Valida sintaxe primeiro
        validation = executor.validate_code(code)
        if not validation['valid']:
            logging.warning(f"Código com erro de sintaxe: {validation['error']}")
            return jsonify({
                "success": False,
                "error": "Erro de sintaxe no código",
                "details": validation['error']
            }), 400
        
        logging.info("Código validado com sucesso. Executando correção...")
        
        # Executa a correção com IA
        correction_result = corrector.correct_exercise(code, exercise_description, lesson_number)
        
        logging.info(f"Correção concluída: {correction_result.get('correct', 'N/A')}")
        
        return jsonify({
            "success": True,
            "correction": correction_result
        }), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logging.error(f"Erro na correção automática: {e}")
        logging.error(f"Traceback completo:\n{error_trace}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "details": str(e)
        }), 500

@api_bp.route("/get-all-progress/<user_id>", methods=["GET"])
def get_all_progress(user_id):
    """Obtém progresso de todos os módulos do usuário"""
    try:
        if not db:
            return jsonify({"error": "Banco de dados não configurado"}), 500
        
        modules = ['sequencial', 'comparativa', 'repetitiva', 'vetores', 'matrizes']
        module_data = {}
        global_stats = {
            'total_completed': 0,
            'total_lessons': 50,  # 10 aulas por módulo × 5 módulos
            'progress_percentage': 0
        }
        
        for module in modules:
            try:
                # Busca progresso do módulo
                doc_ref = db.collection('usuarios').document(user_id).collection('conteudo').document(module)
                doc = doc_ref.get()
                
                if doc.exists:
                    data = doc.to_dict()
                    aulas_concluidas = data.get('aulas_concluidas', [])
                    aulas_liberadas = data.get('aulas_liberadas', [1] if module == 'sequencial' else [])
                    
                    total_completed = len(aulas_concluidas)
                    progress_percentage = (total_completed / 10) * 100
                    
                    module_data[module] = {
                        'total_completed': total_completed,
                        'total_lessons': 10,
                        'progress_percentage': progress_percentage,
                        'aulas_concluidas': aulas_concluidas,
                        'aulas_liberadas': aulas_liberadas
                    }
                    
                    global_stats['total_completed'] += total_completed
                    
                else:
                    # Módulo não existe, cria com dados padrão
                    aulas_liberadas = [1] if module == 'sequencial' else []
                    module_data[module] = {
                        'total_completed': 0,
                        'total_lessons': 10,
                        'progress_percentage': 0,
                        'aulas_concluidas': [],
                        'aulas_liberadas': aulas_liberadas
                    }
                    
                    # Inicializa o documento no Firestore
                    doc_ref.set({
                        'aulas_concluidas': [],
                        'aulas_liberadas': aulas_liberadas,
                        'ultimo_acesso': firestore.SERVER_TIMESTAMP
                    })
                    
            except Exception as e:
                logging.error(f"Erro ao carregar progresso do módulo {module}: {e}")
                # Em caso de erro, retorna dados padrão
                module_data[module] = {
                    'total_completed': 0,
                    'total_lessons': 10,
                    'progress_percentage': 0,
                    'aulas_concluidas': [],
                    'aulas_liberadas': [1] if module == 'sequencial' else []
                }
        
        # Calcula estatísticas globais
        global_stats['progress_percentage'] = (global_stats['total_completed'] / global_stats['total_lessons']) * 100
        
        return jsonify({
            "success": True,
            "modules": module_data,
            "global_stats": global_stats
        })
        
    except Exception as e:
        logging.error(f"Erro ao obter progresso global: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@api_bp.route("/init-user-progress/<user_id>", methods=["POST"])
def init_user_progress(user_id):
    """Inicializa progresso do usuário para todos os módulos"""
    try:
        if not db:
            return jsonify({"error": "Banco de dados não configurado"}), 500
        
        modules = ['sequencial', 'comparativa', 'repetitiva', 'vetores', 'matrizes']
        
        for module in modules:
            doc_ref = db.collection('usuarios').document(user_id).collection('conteudo').document(module)
            doc = doc_ref.get()
            
            if not doc.exists:
                # Só o módulo sequencial começa com aula 1 liberada
                aulas_liberadas = [1] if module == 'sequencial' else []
                
                doc_ref.set({
                    'aulas_concluidas': [],
                    'aulas_liberadas': aulas_liberadas,
                    'ultimo_acesso': firestore.SERVER_TIMESTAMP
                })
        
        return jsonify({"success": True, "message": "Progresso inicializado"})
        
    except Exception as e:
        logging.error(f"Erro ao inicializar progresso: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500