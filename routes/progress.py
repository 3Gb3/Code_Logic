from flask import Blueprint, request, jsonify
from firebase_admin import firestore
import logging

progress_bp = Blueprint('progress', __name__, url_prefix='/api')

# Referência para o banco de dados Firestore
db = None

def set_firestore_client(firestore_client):
    """Define o cliente Firestore para as rotas de progresso"""
    global db
    db = firestore_client

def unlock_next_module(user_id, completed_module):
    """Libera o próximo módulo quando um módulo é completado"""
    try:
        if completed_module not in MODULE_ORDER:
            return
        
        current_index = MODULE_ORDER.index(completed_module)
        
        # Verifica se há um próximo módulo
        if current_index + 1 < len(MODULE_ORDER):
            next_module = MODULE_ORDER[current_index + 1]
            
            # Libera a primeira aula do próximo módulo
            user_ref = db.collection('usuarios').document(user_id)
            next_module_ref = user_ref.collection('conteudo').document(next_module)
            
            # Busca ou cria o documento do próximo módulo
            next_doc = next_module_ref.get()
            if next_doc.exists:
                next_data = next_doc.to_dict()
                aulas_liberadas = next_data.get('aulas_liberadas', [])
                
                # Libera a primeira aula se ainda não estiver liberada
                if 1 not in aulas_liberadas:
                    aulas_liberadas.append(1)
                    aulas_liberadas.sort()
                    
                    next_module_ref.update({
                        'aulas_liberadas': aulas_liberadas,
                        'ultima_atualizacao': firestore.SERVER_TIMESTAMP
                    })
                    
                    logging.info(f"Módulo {next_module} liberado para usuário {user_id}")
            else:
                # Cria o documento do próximo módulo com a primeira aula liberada
                module_names = {
                    'comparativa': 'Estruturas Comparativas',
                    'repetitiva': 'Estruturas Repetitivas',
                    'vetores': 'Vetores',
                    'matrizes': 'Matrizes'
                }
                
                next_module_ref.set({
                    'aulas_concluidas': [],
                    'aulas_liberadas': [1],
                    'criado_em': firestore.SERVER_TIMESTAMP,
                    'ultima_atualizacao': firestore.SERVER_TIMESTAMP,
                    'total_aulas': 10,
                    'nome_modulo': module_names.get(next_module, next_module.title())
                })
                
                logging.info(f"Módulo {next_module} criado e liberado para usuário {user_id}")
    
    except Exception as e:
        logging.error(f"Erro ao liberar próximo módulo: {e}")

# Ordem de dependência dos módulos
MODULE_ORDER = ['sequencial', 'comparativa', 'repetitiva', 'vetores', 'matrizes']

def check_module_prerequisites(user_id, target_module):
    """Verifica se o usuário completou os pré-requisitos para acessar um módulo"""
    logging.info(f"Verificando pré-requisitos para usuário {user_id}, módulo {target_module}")
    
    if not db:
        logging.error("Banco de dados não disponível")
        return False, "Banco de dados não disponível"
    
    # Sequencial sempre está liberado
    if target_module == 'sequencial':
        logging.info(f"Módulo sequencial sempre liberado para usuário {user_id}")
        return True, "Módulo inicial sempre liberado"
    
    # Encontra o índice do módulo alvo
    if target_module not in MODULE_ORDER:
        logging.error(f"Módulo inválido: {target_module}")
        return False, "Módulo inválido"
    
    target_index = MODULE_ORDER.index(target_module)
    
    # Verifica se o módulo anterior foi completado
    previous_module = MODULE_ORDER[target_index - 1]
    
    logging.info(f"Verificando se módulo anterior ({previous_module}) foi completado para liberar {target_module}")
    
    try:
        user_ref = db.collection('usuarios').document(user_id)
        previous_module_ref = user_ref.collection('conteudo').document(previous_module)
        previous_doc = previous_module_ref.get()
        
        if not previous_doc.exists:
            logging.warning(f"Módulo anterior ({previous_module}) não encontrado para usuário {user_id}")
            return False, f"Módulo anterior ({previous_module}) não encontrado"
        
        previous_data = previous_doc.to_dict()
        aulas_concluidas = previous_data.get('aulas_concluidas', [])
        total_aulas = previous_data.get('total_aulas', 10)
        
        logging.info(f"Módulo {previous_module}: {len(aulas_concluidas)}/{total_aulas} aulas concluídas")
        
        # Verifica se todas as aulas do módulo anterior foram concluídas
        if len(aulas_concluidas) >= total_aulas:
            logging.info(f"Módulo {previous_module} completado! Liberando acesso ao {target_module}")
            return True, f"Módulo {previous_module} completado"
        else:
            completed = len(aulas_concluidas)
            message = f"Complete todas as {total_aulas} aulas de {previous_module} primeiro (concluídas: {completed}/{total_aulas})"
            logging.info(f"Acesso negado ao {target_module}: {message}")
            return False, message
    
    except Exception as e:
        logging.error(f"Erro ao verificar pré-requisitos: {e}")
        return False, f"Erro ao verificar pré-requisitos: {str(e)}"

@progress_bp.route("/check-module-access/<user_id>/<module>", methods=["GET"])
def check_module_access(user_id, module):
    """Verifica se o usuário pode acessar um módulo específico"""
    try:
        can_access, message = check_module_prerequisites(user_id, module)
        
        return jsonify({
            "success": True,
            "can_access": can_access,
            "message": message,
            "module": module
        })
        
    except Exception as e:
        logging.error(f"Erro ao verificar acesso ao módulo: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "details": str(e)
        }), 500

@progress_bp.route("/check-module-access/<module>", methods=["GET"])
def check_module_access_query(module):
    """Verifica se o usuário pode acessar um módulo específico (user_id via query parameter)"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({
                "success": False,
                "error": "user_id é obrigatório"
            }), 400
        
        can_access, message = check_module_prerequisites(user_id, module)
        
        return jsonify({
            "success": True,
            "can_access": can_access,
            "message": message,
            "module": module
        })
        
    except Exception as e:
        logging.error(f"Erro ao verificar acesso ao módulo: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "details": str(e)
        }), 500

@progress_bp.route("/init-progress", methods=["POST"])
def init_progress():
    """Inicializa o progresso do usuário no Firestore para todos os módulos"""
    try:
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({"error": "user_id é obrigatório"}), 400
        
        user_id = data['user_id']
        
        if not db:
            return jsonify({"error": "Banco de dados não disponível"}), 500
        
        # Referência para a estrutura do usuário
        user_ref = db.collection('usuarios').document(user_id)
        
        # Módulos de conteúdo
        modules = {
            'sequencial': {'total_aulas': 10, 'nome': 'Programação Sequencial'},
            'comparativa': {'total_aulas': 10, 'nome': 'Estruturas Comparativas'},
            'repetitiva': {'total_aulas': 10, 'nome': 'Estruturas Repetitivas'},
            'vetores': {'total_aulas': 10, 'nome': 'Vetores'},
            'matrizes': {'total_aulas': 10, 'nome': 'Matrizes'}
        }
        
        for module_name, module_info in modules.items():
            conteudo_ref = user_ref.collection('conteudo').document(module_name)
            
            # Verifica se já existe
            doc = conteudo_ref.get()
            if not doc.exists:
                # Dados iniciais para cada módulo
                # Só o sequencial começa com aula liberada
                aulas_liberadas = [1] if module_name == 'sequencial' else []
                
                initial_data = {
                    'aulas_concluidas': [],
                    'aulas_liberadas': aulas_liberadas,
                    'criado_em': firestore.SERVER_TIMESTAMP,
                    'ultima_atualizacao': firestore.SERVER_TIMESTAMP,
                    'total_aulas': module_info['total_aulas'],
                    'nome_modulo': module_info['nome']
                }
                conteudo_ref.set(initial_data)
        
        logging.info(f"Progresso inicializado para todos os módulos do usuário {user_id}")
        
        return jsonify({
            "success": True,
            "message": "Progresso inicializado para todos os módulos"
        })
        
    except Exception as e:
        logging.error(f"Erro ao inicializar progresso: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "details": str(e)
        }), 500

@progress_bp.route("/complete-lesson", methods=["POST"])
def complete_lesson():
    """Marca uma aula como concluída e libera a próxima"""
    try:
        data = request.get_json()
        if not data or 'lesson_number' not in data or 'user_id' not in data:
            return jsonify({"error": "Dados incompletos"}), 400
        
        lesson_number = data['lesson_number']
        user_id = data['user_id']
        module = data.get('module', 'sequencial')  # Módulo padrão é sequencial
        
        if not db:
            return jsonify({"error": "Banco de dados não disponível"}), 500
        
        # Nova estrutura: usuarios/{user_id}/conteudo/{module}
        user_ref = db.collection('usuarios').document(user_id)
        conteudo_ref = user_ref.collection('conteudo').document(module)
        
        # Busca o documento atual ou cria se não existir
        conteudo_doc = conteudo_ref.get()
        if conteudo_doc.exists:
            conteudo_data = conteudo_doc.to_dict()
            aulas_concluidas = conteudo_data.get('aulas_concluidas', [])
            aulas_liberadas = conteudo_data.get('aulas_liberadas', [1])
            total_aulas = conteudo_data.get('total_aulas', 10)
        else:
            aulas_concluidas = []
            aulas_liberadas = [1]  # Primeira aula sempre liberada
            total_aulas = 10
        
        # Verifica se a aula está liberada
        if lesson_number not in aulas_liberadas:
            return jsonify({
                "success": False,
                "error": f"Aula {lesson_number} não está liberada ainda"
            }), 403
        
        # Adiciona a aula à lista se ainda não estiver
        if lesson_number not in aulas_concluidas:
            aulas_concluidas.append(lesson_number)
            aulas_concluidas.sort()  # Mantém a lista ordenada
            
            # Libera a próxima aula (se existir)
            next_lesson = lesson_number + 1
            if next_lesson <= total_aulas and next_lesson not in aulas_liberadas:
                aulas_liberadas.append(next_lesson)
                aulas_liberadas.sort()
            
            # Verifica se o módulo foi completado e libera o próximo módulo
            if len(aulas_concluidas) == total_aulas:
                # Módulo completado! Libera o próximo módulo
                unlock_next_module(user_id, module)
        
        # Atualiza o documento
        conteudo_data = {
            'aulas_concluidas': aulas_concluidas,
            'aulas_liberadas': aulas_liberadas,
            'ultima_atualizacao': firestore.SERVER_TIMESTAMP,
            'total_aulas': total_aulas
        }
        
        conteudo_ref.set(conteudo_data, merge=True)
        
        total_completed = len(aulas_concluidas)
        progress_percentage = (total_completed / total_aulas) * 100
        
        return jsonify({
            "success": True,
            "message": f"Aula {lesson_number} marcada como concluída",
            "aulas_concluidas": aulas_concluidas,
            "aulas_liberadas": aulas_liberadas,
            "total_completed": total_completed,
            "progress_percentage": progress_percentage,
            "next_lesson_unlocked": lesson_number + 1 if lesson_number + 1 <= total_aulas else None
        })
        
    except Exception as e:
        logging.error(f"Erro ao marcar aula como concluída: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "details": str(e)
        }), 500

@progress_bp.route("/get-progress/<user_id>/<module>", methods=["GET"])
def get_progress_by_module(user_id, module):
    """Obter progresso de um módulo específico"""
    try:
        if not db:
            return jsonify({"error": "Banco de dados não disponível"}), 500
        
        # Verifica se o usuário pode acessar este módulo
        can_access, access_message = check_module_prerequisites(user_id, module)
        
        # Estrutura: usuarios/{user_id}/conteudo/{module}
        user_ref = db.collection('usuarios').document(user_id)
        conteudo_ref = user_ref.collection('conteudo').document(module)
        
        # Busca o documento de conteúdo
        conteudo_doc = conteudo_ref.get()
        if conteudo_doc.exists:
            conteudo_data = conteudo_doc.to_dict()
            aulas_concluidas = conteudo_data.get('aulas_concluidas', [])
            aulas_liberadas = conteudo_data.get('aulas_liberadas', [])
            total_aulas = conteudo_data.get('total_aulas', 10)
            nome_modulo = conteudo_data.get('nome_modulo', module.title())
        else:
            aulas_concluidas = []
            # Se não pode acessar o módulo, não libera nenhuma aula
            aulas_liberadas = [1] if can_access else []
            total_aulas = 10
            nome_modulo = module.title()
        
        # Se não pode acessar o módulo, limpa as aulas liberadas
        if not can_access:
            aulas_liberadas = []
        
        total_completed = len(aulas_concluidas)
        progress_percentage = (total_completed / total_aulas) * 100
        
        # Determina qual é a próxima aula disponível
        next_lesson = None
        if can_access:
            for i in range(1, total_aulas + 1):
                if i in aulas_liberadas and i not in aulas_concluidas:
                    next_lesson = i
                    break
        
        return jsonify({
            "success": True,
            "module": module,
            "nome_modulo": nome_modulo,
            "aulas_concluidas": aulas_concluidas,
            "aulas_liberadas": aulas_liberadas,
            "total_completed": total_completed,
            "total_lessons": total_aulas,
            "progress_percentage": progress_percentage,
            "next_lesson": next_lesson,
            "can_access": can_access,
            "access_message": access_message
        })
        
    except Exception as e:
        logging.error(f"Erro ao obter progresso do módulo {module}: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "details": str(e)
        }), 500

@progress_bp.route("/get-all-progress/<user_id>", methods=["GET"])
def get_all_progress(user_id):
    """Obter progresso de todos os módulos"""
    try:
        logging.info(f"Carregando progresso para usuário: {user_id}")
        
        if not db:
            return jsonify({"error": "Banco de dados não disponível"}), 500
        
        # Lista de módulos
        modules = ['sequencial', 'comparativa', 'repetitiva', 'vetores', 'matrizes']
        progress_data = {}
        total_global_completed = 0
        total_global_lessons = 0
        
        user_ref = db.collection('usuarios').document(user_id)
        
        for module in modules:
            conteudo_ref = user_ref.collection('conteudo').document(module)
            conteudo_doc = conteudo_ref.get()
            
            if conteudo_doc.exists:
                conteudo_data = conteudo_doc.to_dict()
                aulas_concluidas = conteudo_data.get('aulas_concluidas', [])
                aulas_liberadas = conteudo_data.get('aulas_liberadas', [1])
                total_aulas = conteudo_data.get('total_aulas', 10)
                nome_modulo = conteudo_data.get('nome_modulo', module.title())
                
                logging.info(f"Módulo {module}: {len(aulas_concluidas)} aulas concluídas - {aulas_concluidas}")
            else:
                aulas_concluidas = []
                aulas_liberadas = [1]
                total_aulas = 10
                nome_modulo = module.title()
                
                logging.info(f"Módulo {module}: documento não existe, criando dados padrão")
            
            total_completed = len(aulas_concluidas)
            progress_percentage = (total_completed / total_aulas) * 100
            
            # Próxima aula disponível
            next_lesson = None
            for i in range(1, total_aulas + 1):
                if i in aulas_liberadas and i not in aulas_concluidas:
                    next_lesson = i
                    break
            
            progress_data[module] = {
                "nome_modulo": nome_modulo,
                "aulas_concluidas": aulas_concluidas,
                "aulas_liberadas": aulas_liberadas,
                "total_completed": total_completed,
                "total_lessons": total_aulas,
                "progress_percentage": progress_percentage,
                "next_lesson": next_lesson
            }
            
            total_global_completed += total_completed
            total_global_lessons += total_aulas
        
        global_progress_percentage = (total_global_completed / total_global_lessons) * 100 if total_global_lessons > 0 else 0
        
        logging.info(f"Progresso global: {total_global_completed}/{total_global_lessons} ({global_progress_percentage:.1f}%)")
        
        return jsonify({
            "success": True,
            "modules": progress_data,
            "global_stats": {
                "total_completed": total_global_completed,
                "total_lessons": total_global_lessons,
                "progress_percentage": global_progress_percentage
            }
        })
        
    except Exception as e:
        logging.error(f"Erro ao obter progresso global: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "details": str(e)
        }), 500

@progress_bp.route("/test-firestore/<user_id>", methods=["GET"])
def test_firestore(user_id):
    """Teste da estrutura do Firestore"""
    try:
        if not db:
            return jsonify({"error": "Banco de dados não disponível"}), 500
        
        # Testa criação da estrutura
        user_ref = db.collection('usuarios').document(user_id)
        conteudo_ref = user_ref.collection('conteudo').document('sequencial')
        
        # Cria estrutura de teste
        test_data = {
            'aulas_concluidas': [1, 2],
            'aulas_liberadas': [1, 2, 3],
            'criado_em': firestore.SERVER_TIMESTAMP,
            'ultima_atualizacao': firestore.SERVER_TIMESTAMP,
            'total_aulas': 10
        }
        conteudo_ref.set(test_data)
        
        # Lê de volta para verificar
        doc = conteudo_ref.get()
        if doc.exists:
            return jsonify({
                "success": True,
                "message": "Estrutura criada e verificada com sucesso",
                "data": doc.to_dict()
            })
        else:
            return jsonify({"success": False, "error": "Falha ao criar estrutura"})
            
    except Exception as e:
        logging.error(f"Erro no teste do Firestore: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor",
            "details": str(e)
        }), 500