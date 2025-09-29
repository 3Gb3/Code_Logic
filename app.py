from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth, firestore
import logging
import os
import sys
from dotenv import load_dotenv

# Importar Blueprints
from routes.auth import auth_bp
from routes.aulas import aulas_bp, set_firestore_client as set_aulas_firestore
from routes.exercicios import exercicios_bp
from routes.api import api_bp, set_firestore_client as set_api_firestore
from routes.progress import progress_bp, set_firestore_client as set_progress_firestore

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Função para verificar e ajustar tempo do sistema
def check_system_time():
    """Verifica se o relógio do sistema está sincronizado"""
    try:
        import time
        import requests
        
        # Pega o tempo atual do sistema
        local_time = time.time()
        
        # Tenta pegar o tempo de um servidor NTP via HTTP (mais simples que NTP direto)
        try:
            response = requests.get('http://worldtimeapi.org/api/timezone/UTC', timeout=5)
            if response.status_code == 200:
                data = response.json()
                server_time = data['unixtime']
                time_diff = abs(local_time - server_time)
                
                if time_diff > 5:  # Diferença maior que 5 segundos
                    app.logger.warning(f"Clock skew detectado: {time_diff:.2f} segundos de diferença")
                    return False
        except:
            pass  # Se não conseguir verificar, continua normalmente
            
        return True
    except Exception as e:
        app.logger.warning(f"Não foi possível verificar sincronização de tempo: {e}")
        return True  # Assume que está ok se não conseguir verificar

# Inicializa Firebase Admin com service account
service_account_path = os.path.join(os.path.dirname(__file__), "chave_firebase.json")
if not os.path.exists(service_account_path):
    print(f"ERRO: service-account.json não encontrado em {service_account_path}")
    sys.exit(1)

# Configurações do Firebase com tolerância de clock skew
cred = credentials.Certificate(service_account_path)

# Inicializa app Firebase 
try:
    firebase_app = firebase_admin.initialize_app(cred)
    print("✅ Firebase inicializado com sucesso")
    
    # Inicializa Firestore
    db = firestore.client()
    print("✅ Firestore inicializado com sucesso")
    
    # Injeta o cliente Firestore nos Blueprints
    set_api_firestore(db)
    set_progress_firestore(db)
    set_aulas_firestore(db)
    
except Exception as e:
    print(f"⚠️  Aviso Firebase: {e}")
    # Mesmo com erro, continua - pode ser apenas clock skew
    try:
        firebase_app = firebase_admin.initialize_app(cred)
        db = firestore.client()
        # Injeta o cliente Firestore nos Blueprints
        set_api_firestore(db)
        set_progress_firestore(db)
        set_aulas_firestore(db)
    except:
        db = None
        print("❌ Firestore não disponível")

# Verifica sincronização de tempo na inicialização
time_sync_ok = check_system_time()
if not time_sync_ok:
    print("⚠️  AVISO: Detectada diferença de tempo. Se houver erros de token, sincronize o relógio do sistema.")

# Registrar Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(aulas_bp)
app.register_blueprint(exercicios_bp)
app.register_blueprint(api_bp)
app.register_blueprint(progress_bp)

print("Static folder:", app.static_folder)

# Handler global para erros HTTP que retorna JSON
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Rota não encontrada"}), 404

@app.errorhandler(500)
def internal_error(e):
    app.logger.error(f"Erro interno: {e}")
    return jsonify({"error": "Erro interno do servidor"}), 500

if __name__ == "__main__":
    # Ativa logging para debug
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)