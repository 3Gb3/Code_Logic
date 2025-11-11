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
    
    def execute_python_code(self, code, inputs=None):
        """
        Executa código Python de forma segura
        Args:
            code: Código Python a ser executado
            inputs: Lista de valores de entrada para input() ou None
        Retorna: dict com success, output, error, input_needed
        """
        try:
            # Se não foram fornecidos inputs, detecta se o código precisa deles
            if inputs is None:
                input_count = code.count('input(')
                if input_count > 0:
                    return {
                        'success': False,
                        'output': '',
                        'error': None,
                        'input_needed': True,
                        'input_count': input_count,
                        'message': f'Este código precisa de {input_count} valor(es) de entrada. Por favor, forneça os valores.'
                    }
            
            # Captura stdout e stderr
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            # Cria um iterador para os inputs
            input_iterator = iter(inputs if inputs else [])
            
            def mock_input(prompt=""):
                """Input simulado que usa valores pré-fornecidos"""
                try:
                    value = next(input_iterator)
                    # Imprime o prompt e o valor fornecido
                    print(f"{prompt}{value}")
                    return str(value)
                except StopIteration:
                    raise RuntimeError("Não há valores de entrada suficientes fornecidos")
            
            # Cria um namespace limpo para execução
            namespace = {
                '__builtins__': {
                    'print': print,
                    'input': mock_input,  # input simulado
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
                'error': error if error else None,
                'input_needed': False
            }
            
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e) + '\n' + traceback.format_exc(),
                'input_needed': False
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