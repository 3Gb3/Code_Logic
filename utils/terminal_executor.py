"""
Executor de código Python com terminal interativo
Suporta input() em tempo real via WebSocket
"""

import sys
import io
import traceback
import threading
from contextlib import redirect_stdout, redirect_stderr
from queue import Queue, Empty


class InteractiveExecutor:
    """Executor que permite interação em tempo real com o código"""
    
    def __init__(self, socketio, session_id):
        self.socketio = socketio
        self.session_id = session_id
        self.input_queue = Queue()
        self.should_stop = False
        self.is_cancelled = False
        self.execution_thread = None
    
    def cleanup(self):
        """Limpa recursos do executor"""
        import sys
        sys.stdout.write(f"[CLEANUP] Limpando executor {self.session_id[:8]}\n")
        sys.stdout.flush()
        
        self.is_cancelled = True
        
        # Limpa a fila de input e desbloqueia wait_for_input
        while not self.input_queue.empty():
            try:
                self.input_queue.get_nowait()
            except:
                break
        
        # Coloca um valor vazio para desbloquear qualquer get() pendente
        try:
            self.input_queue.put_nowait("")
        except:
            pass
        
        sys.stdout.write(f"[CLEANUP] Limpeza completa\n")
        sys.stdout.flush()
        
    def wait_for_input(self, prompt=""):
        """Aguarda input do usuário via WebSocket"""
        import sys
        sys.stdout.write(f"[WAIT_INPUT] Solicitando input com prompt: {repr(prompt)}\n")
        sys.stdout.flush()
        
        # Envia solicitação de input para o cliente
        self.socketio.emit('request_input', {'prompt': prompt}, room=self.session_id)
        
        # Aguarda resposta do usuário (com timeout)
        try:
            sys.stdout.write(f"[WAIT_INPUT] Aguardando resposta na fila...\n")
            sys.stdout.flush()
            
            user_input = self.input_queue.get(timeout=5)  # Timeout de 5 segundos para testar
            
            sys.stdout.write(f"[WAIT_INPUT] Recebido: {repr(user_input)}\n")
            sys.stdout.flush()
            
            # Verifica se foi cancelado
            if self.is_cancelled:
                sys.stdout.write(f"[WAIT_INPUT] Foi cancelado!\n")
                sys.stdout.flush()
                raise KeyboardInterrupt("Execução cancelada")
                
            return str(user_input)
        except Empty:
            sys.stdout.write(f"[WAIT_INPUT] TIMEOUT aguardando entrada!\n")
            sys.stdout.flush()
            raise TimeoutError("Timeout aguardando entrada do usuário")
    
    def provide_input(self, user_input):
        """Fornece input do usuário para o código em execução"""
        if not self.is_cancelled:
            self.input_queue.put(user_input)
    
    def cancel(self):
        """Cancela a execução atual"""
        self.is_cancelled = True
        # Desbloqueia wait_for_input se estiver esperando
        try:
            self.input_queue.put("")
        except:
            pass
    
    def execute(self, code):
        """Executa código Python com suporte a input interativo"""
        import sys
        sys.stdout.write(f"[EXECUTE] Iniciando execução, cancelado={self.is_cancelled}\n")
        sys.stdout.flush()
        
        try:
            # Verifica se foi cancelado antes de começar
            if self.is_cancelled:
                sys.stdout.write(f"[EXECUTE] Já estava cancelado!\n")
                sys.stdout.flush()
                return {
                    'success': False,
                    'output': '',
                    'error': 'Execução cancelada antes de iniciar'
                }
            
            # Cria namespace com input interativo
            # Importa builtins padrão e sobrescreve print e input
            import builtins
            
            custom_builtins = {
                'print': self._make_print_function(),
                'input': self.wait_for_input,
            }
            
            # Cria um dict que herda de builtins e adiciona nossas customizações
            namespace = {
                '__builtins__': {**vars(builtins), **custom_builtins}
            }
            
            exec(code, namespace)
            
            # Verifica se foi cancelado após execução
            if self.is_cancelled:
                return {
                    'success': False,
                    'output': '',
                    'error': 'Execução cancelada'
                }
            
            return {
                'success': True,
                'output': '',
                'error': None
            }
            
        except KeyboardInterrupt:
            return {
                'success': False,
                'output': '',
                'error': 'Execução cancelada pelo usuário'
            }
        except Exception as e:
            error_trace = traceback.format_exc()
            error_message = f"{str(e)}\n{error_trace}"
            # Envia erro para o terminal também
            self.socketio.emit('output', {'data': f"\n{error_message}"}, room=self.session_id)
            return {
                'success': False,
                'output': '',
                'error': error_message
            }
    
    def _make_print_function(self):
        """Cria função print que envia output via WebSocket em tempo real"""
        socketio = self.socketio
        session_id = self.session_id
        
        def custom_print(*args, **kwargs):
            # Log temporário para debug
            import sys
            sys.stdout.write(f"[CUSTOM_PRINT] Args: {args}\n")
            sys.stdout.flush()
            
            # Converte args para string como print normal faria
            sep = kwargs.get('sep', ' ')
            end = kwargs.get('end', '\n')
            output = sep.join(str(arg) for arg in args) + end
            
            sys.stdout.write(f"[CUSTOM_PRINT] Output: {repr(output)}\n")
            sys.stdout.flush()
            
            # Converte \n para \r\n para o terminal
            output = output.replace('\n', '\r\n')
            
            sys.stdout.write(f"[CUSTOM_PRINT] Enviando para {session_id}\n")
            sys.stdout.flush()
            
            # Envia output para o cliente via WebSocket
            try:
                socketio.emit('output', {'data': output}, room=session_id)
                socketio.sleep(0)  # Força flush do SocketIO
                sys.stdout.write(f"[CUSTOM_PRINT] Enviado com sucesso!\n")
                sys.stdout.flush()
            except Exception as e:
                sys.stdout.write(f"[CUSTOM_PRINT] ERRO: {e}\n")
                sys.stdout.flush()
        
        return custom_print


class ExecutionThread(threading.Thread):
    """Thread para executar código de forma não-bloqueante"""
    
    def __init__(self, executor, code, callback):
        super().__init__(daemon=True)
        self.executor = executor
        self.code = code
        self.callback = callback
    
    def run(self):
        result = self.executor.execute(self.code)
        self.callback(result)
