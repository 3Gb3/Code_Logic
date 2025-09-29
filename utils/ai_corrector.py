"""
Sistema de correção automática de exercícios usando IA
"""
import os
from openai import OpenAI
from typing import Dict, Any
import json
import logging

class AICorrector:
    def __init__(self):
        # Para desenvolvimento, sempre usar modo mock
        # Remova esta linha quando tiver uma chave API real
        self.mock_mode = True
        
        # Inicializa o cliente OpenAI
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            api_key = "sk-mock-key-for-development"
            logging.warning("OPENAI_API_KEY não encontrada. Usando modo de desenvolvimento.")
        
        # Só inicializa o cliente se não estiver em modo mock
        if not self.mock_mode:
            try:
                self.client = OpenAI(api_key=api_key)
            except Exception as e:
                logging.warning(f"Erro ao inicializar OpenAI: {e}. Usando modo mock.")
                self.mock_mode = True
    
    def correct_exercise(self, student_code: str, exercise_description: str, lesson_number: int) -> Dict[str, Any]:
        """
        Corrige um exercício do aluno usando IA
        
        Args:
            student_code: O código submetido pelo aluno
            exercise_description: Descrição do exercício/tarefa
            lesson_number: Número da aula (1-10)
        
        Returns:
            Dict com 'correct', 'feedback', 'score' e 'suggestions'
        """
        try:
            if self.mock_mode:
                return self._mock_correction(student_code, exercise_description)
            
            # Prompt para a IA
            system_prompt = """Você é um professor de programação Python especializado em corrigir exercícios básicos de programação sequencial. 

Sua tarefa é:
1. Analisar se o código do aluno resolve corretamente o exercício proposto
2. Dar feedback construtivo sem entregar a solução completa
3. Fornecer dicas direcionais para melhorar

Responda SEMPRE em formato JSON com esta estrutura:
{
    "correct": true/false,
    "feedback": "mensagem para o aluno",
    "score": 0-100,
    "suggestions": ["dica1", "dica2"]
}

Regras:
- Se correto: feedback positivo e motivador
- Se incorreto: explicar o que está errado + dica para correção (SEM dar a solução completa)
- Score: 0-100 baseado na correção e qualidade do código
- Suggestions: máximo 3 dicas práticas
- Seja encorajador e didático
- Foque apenas no exercício proposto"""

            user_prompt = f"""EXERCÍCIO:
{exercise_description}

CÓDIGO DO ALUNO:
```python
{student_code}
```

Analise se o código resolve corretamente o exercício e forneça feedback educativo."""

            # Chama a API do OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Modelo mais barato
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            # Parse da resposta
            ai_response = response.choices[0].message.content.strip()
            
            try:
                result = json.loads(ai_response)
                # Valida a estrutura da resposta
                required_keys = ['correct', 'feedback', 'score', 'suggestions']
                if not all(key in result for key in required_keys):
                    raise ValueError("Resposta da IA incompleta")
                
                # Sanitiza os dados
                result['correct'] = bool(result['correct'])
                result['score'] = max(0, min(100, int(result['score'])))
                result['suggestions'] = result['suggestions'][:3]  # Máximo 3 sugestões
                
                return result
                
            except (json.JSONDecodeError, ValueError) as e:
                logging.error(f"Erro ao parsear resposta da IA: {e}")
                return self._fallback_response(student_code)
                
        except Exception as e:
            logging.error(f"Erro na correção automática: {e}")
            return self._fallback_response(student_code)
    
    def _mock_correction(self, student_code: str, exercise_description: str) -> Dict[str, Any]:
        """Correção mock para desenvolvimento/teste com lógica educativa"""
        code_lower = student_code.lower().strip()
        code_lines = [line.strip() for line in student_code.strip().split('\n') if line.strip()]
        
        # Detecta o tipo de exercício pela descrição
        if "aula 1" in exercise_description.lower():
            return self._check_aula1(code_lower, code_lines)
        elif "aula 2" in exercise_description.lower():
            return self._check_aula2(code_lower, code_lines, student_code)
        else:
            # Análise genérica para outras aulas
            return self._check_generic(code_lower, code_lines)
    
    def _check_aula1(self, code_lower: str, code_lines: list) -> Dict[str, Any]:
        """Análise específica para Aula 1 - Print e Hello World"""
        has_print = 'print(' in code_lower
        print_count = code_lower.count('print(')
        has_hello = 'olá' in code_lower or 'hello' in code_lower
        has_name = any(word in code_lower for word in ['nome', 'name', 'joão', 'maria', 'ana'])
        has_age = any(word in code_lower for word in ['idade', 'age', 'anos', 'years', '20', '18', '25'])
        code_length = len(code_lines)
        
        # Verifica se é a tarefa 1 (só olá mundo)
        if code_length == 1 and has_hello and has_print and print_count == 1:
            return {
                "correct": True,
                "feedback": "Perfeito! Você executou com sucesso seu primeiro programa em Python! O comando print() exibiu a mensagem na tela exatamente como esperado.",
                "score": 90,
                "suggestions": [
                    "Agora tente modificar a mensagem",
                    "Experimente adicionar mais comandos print()",
                    "Continue para a próxima tarefa!"
                ]
            }
        
        # Verifica se completou todas as tarefas
        if has_print and print_count >= 3 and has_name and has_age:
            return {
                "correct": True,
                "feedback": "Excelente trabalho! Você completou todas as tarefas: usou print() corretamente, incluiu seu nome e idade, e criou múltiplas mensagens. Seus primeiros passos na programação estão ótimos!",
                "score": 95,
                "suggestions": [
                    "Perfeito! Continue assim",
                    "Tente experimentar mensagens diferentes",
                    "Você está pronto para a próxima aula"
                ]
            }
        
        # Análises de casos incompletos...
        if not has_print:
            return {
                "correct": False,
                "feedback": "Parece que seu código não está usando print() corretamente. Lembre-se: o comando print() é usado para exibir mensagens na tela. Comece com print('Olá, mundo!')",
                "score": 20,
                "suggestions": [
                    "Comece com print('Olá, mundo!')",
                    "Releia as instruções do exercício",
                    "Peça ajuda se precisar!"
                ]
            }
        
        if print_count < 3:
            return {
                "correct": False,
                "feedback": f"Você está no caminho certo usando print()! Mas precisa criar pelo menos 3 mensagens diferentes. Você tem {print_count} print(s), precisa de pelo menos 3.",
                "score": 55,
                "suggestions": [
                    f"Adicione mais {3-print_count} comando(s) print()",
                    "Inclua uma mensagem com seu nome e idade",
                    "Cada print() vai para uma linha diferente"
                ]
            }
        
        return {
            "correct": False,
            "feedback": "Você está progredindo! Continue praticando com os comandos print().",
            "score": 60,
            "suggestions": [
                "Verifique se completou todas as 3 tarefas",
                "Inclua nome e idade em uma das mensagens",
                "Use pelo menos 3 comandos print() diferentes"
            ]
        }
    
    def _check_aula2(self, code_lower: str, code_lines: list, original_code: str) -> Dict[str, Any]:
        """Análise específica para Aula 2 - Variáveis e Tipos"""
        has_variables = any(char in code_lower for char in ['='])
        has_print = 'print(' in code_lower
        has_type = 'type(' in code_lower
        
        # Conta tipos de dados
        has_string = any(quote in original_code for quote in ['"', "'"])
        has_int = any(num in code_lower for num in ['18', '19', '20', '21', '22', '23', '24', '25'])
        has_float = '.' in original_code and any(char.isdigit() for char in original_code)
        has_bool = any(bool_val in code_lower for bool_val in ['true', 'false'])
        
        type_count = sum([has_string, has_int, has_float, has_bool])
        
        if not has_variables:
            return {
                "correct": False,
                "feedback": "Você precisa criar variáveis! Use o símbolo = para atribuir valores às variáveis. Exemplo: nome = 'João'",
                "score": 25,
                "suggestions": [
                    "Use o símbolo = para criar variáveis",
                    "Crie uma variável para nome, idade, altura e se gosta de programar",
                    "Exemplo: nome = 'Seu Nome'"
                ]
            }
        
        if type_count < 4:
            missing_types = []
            if not has_string: missing_types.append("string (texto entre aspas)")
            if not has_int: missing_types.append("inteiro (número sem ponto)")
            if not has_float: missing_types.append("float (número com ponto decimal)")
            if not has_bool: missing_types.append("boolean (True ou False)")
            
            return {
                "correct": False,
                "feedback": f"Você precisa criar variáveis com todos os 4 tipos de dados. Ainda falta: {', '.join(missing_types)}",
                "score": 40 + (type_count * 10),
                "suggestions": [
                    f"Crie variáveis com: {', '.join(missing_types)}",
                    "Exemplo: altura = 1.75 (float)",
                    "Exemplo: gosta_programar = True (boolean)"
                ]
            }
        
        if not has_print:
            return {
                "correct": False,
                "feedback": "Ótimo! Você criou as variáveis. Agora use print() para exibir os valores de cada uma.",
                "score": 60,
                "suggestions": [
                    "Use print(nome) para exibir a variável nome",
                    "Faça isso para todas as 4 variáveis",
                    "Cada print() em uma linha separada"
                ]
            }
        
        if not has_type:
            return {
                "correct": False,
                "feedback": "Muito bem! Você criou as variáveis e as exibiu. Agora use type() para mostrar o tipo de cada variável. Exemplo: print(type(nome))",
                "score": 75,
                "suggestions": [
                    "Use print(type(nome)) para mostrar o tipo",
                    "Faça isso para todas as 4 variáveis",
                    "type() mostra qual é o tipo da variável"
                ]
            }
        
        # Se chegou até aqui, está completo
        return {
            "correct": True,
            "feedback": "Excelente! Você dominou variáveis e tipos de dados! Criou os 4 tipos principais, exibiu os valores e mostrou os tipos. Está pronto para conceitos mais avançados!",
            "score": 95,
            "suggestions": [
                "Perfeito domínio de variáveis!",
                "Experimente criar outras variáveis",
                "Você está pronto para a próxima aula"
            ]
        }
    
    def _check_generic(self, code_lower: str, code_lines: list) -> Dict[str, Any]:
        """Análise genérica para outras aulas"""
        if len(code_lines) < 2:
            return {
                "correct": False,
                "feedback": "Seu código parece muito simples. Verifique se está implementando tudo que foi pedido no exercício.",
                "score": 30,
                "suggestions": [
                    "Releia a descrição do exercício",
                    "Implemente todas as funcionalidades pedidas",
                    "Teste seu código antes de enviar"
                ]
            }
        elif 'print(' in code_lower:
            return {
                "correct": True,
                "feedback": "Bom trabalho! Seu código está funcionando corretamente.",
                "score": 85,
                "suggestions": [
                    "Continue praticando!",
                    "Tente otimizar seu código",
                    "Explore diferentes soluções"
                ]
            }
        else:
            return {
                "correct": False,
                "feedback": "Verifique se seu código está completo e testado.",
                "score": 50,
                "suggestions": [
                    "Teste seu código manualmente",
                    "Verifique se há erros de sintaxe",
                    "Confira se a lógica está correta"
                ]
            }
    
    def _fallback_response(self, student_code: str) -> Dict[str, Any]:
        """Resposta de fallback quando a IA falha"""
        return {
            "correct": None,  # Indica que não foi possível avaliar
            "feedback": "Não foi possível avaliar automaticamente seu código. Verifique se está funcionando corretamente e tente novamente.",
            "score": 50,
            "suggestions": [
                "Teste seu código manualmente",
                "Verifique se não há erros de sintaxe",
                "Confira se a lógica está correta"
            ]
        }

# Instância global do corretor
corrector = AICorrector()