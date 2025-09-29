import sys
import io
import traceback
import subprocess
import tempfile
import os
from contextlib import redirect_stdout, redirect_stderr

class CodeExecutor:
    def __init__(self):
        self.timeout = 10  # timeout em segundos
    
    def execute_python_code(self, code):
        """
        Executa código Python de forma segura
        Retorna: dict com success, output, error
        """
        try:
            # Captura stdout e stderr
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            # Cria um namespace limpo para execução
            namespace = {
                '__builtins__': {
                    'print': print,
                    'input': lambda x="": x,  # input seguro
                    'len': len,
                    'str': str,
                    'int': int,
                    'float': float,
                    'bool': bool,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple,
                    'set': set,
                    'range': range,
                    'enumerate': enumerate,
                    'zip': zip,
                    'sum': sum,
                    'max': max,
                    'min': min,
                    'abs': abs,
                    'round': round,
                    'sorted': sorted,
                    'reversed': reversed,
                    'type': type,
                    'isinstance': isinstance,
                }
            }
            
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, namespace)
            
            output = stdout_capture.getvalue()
            error = stderr_capture.getvalue()
            
            return {
                'success': True,
                'output': output,
                'error': error if error else None
            }
            
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e) + '\n' + traceback.format_exc()
            }
    
    def validate_code(self, code):
        """
        Valida se o código tem sintaxe válida
        """
        try:
            compile(code, '<string>', 'exec')
            return {'valid': True, 'error': None}
        except SyntaxError as e:
            return {
                'valid': False, 
                'error': f"Erro de sintaxe na linha {e.lineno}: {e.msg}"
            }
        except Exception as e:
            return {'valid': False, 'error': str(e)}

# Instância global do executor
executor = CodeExecutor()