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
        # Modo desenvolvedor ativado - usando correção mock educativa
        self.mock_mode = True
        
        # Inicializa o cliente OpenAI
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logging.info("💡 OPENAI_API_KEY não configurada. Usando modo de desenvolvimento (mock).")
            self.mock_mode = True
        
        # Só inicializa o cliente se não estiver em modo mock
        if not self.mock_mode:
            try:
                self.client = OpenAI(api_key=api_key)
                logging.info("✅ OpenAI API inicializada com sucesso")
            except Exception as e:
                logging.warning(f"Erro ao inicializar OpenAI: {e}. Usando modo mock.")
                self.mock_mode = True
        else:
            logging.info("🎯 Modo de desenvolvimento ativo - Usando correção educativa local")
    
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
            # Log da requisição
            logging.info(f"🔍 Iniciando correção - Aula {lesson_number}")
            logging.info(f"   Código: {len(student_code)} caracteres")
            logging.info(f"   Descrição: {len(exercise_description)} caracteres")
            logging.info(f"   Modo Mock: {self.mock_mode}")
            
            if self.mock_mode:
                return self._mock_correction(student_code, exercise_description)
            
            # Prompt melhorado para a IA
            system_prompt = """Você é um professor de programação Python experiente e didático, especializado em corrigir exercícios de alunos iniciantes.

Sua tarefa é analisar o código do aluno comparando com o exercício proposto. 

IMPORTANTE:
1. Leia TODA a descrição do exercício, incluindo exemplos de entrada/saída
2. Identifique TODAS as tarefas que o aluno deve completar
3. Verifique se o código do aluno implementa CADA tarefa corretamente
4. Compare os exemplos fornecidos com o que o código produziria
5. Se houver exemplos de saída esperada, o código DEVE produzir exatamente aquela saída

Responda SEMPRE em formato JSON com esta estrutura:
{
    "correct": true/false,
    "feedback": "mensagem detalhada para o aluno",
    "score": 0-100,
    "suggestions": ["dica1", "dica2", "dica3"]
}

Critérios de avaliação:
- correct: true APENAS se o código resolve TODAS as tarefas corretamente
- feedback: Explique o que está certo/errado, mencione tarefas faltantes
- score: 
  * 90-100: Perfeito, todas as tarefas completas
  * 70-89: Bom, tarefas principais feitas, mas pode melhorar
  * 50-69: Incompleto, algumas tarefas faltando
  * 30-49: Código parcial, várias tarefas faltando
  * 0-29: Código muito incompleto ou com erros graves
- suggestions: Máximo 3 dicas práticas e específicas

Seja encorajador mas honesto. Se está errado, explique o porquê."""

            user_prompt = f"""DESCRIÇÃO COMPLETA DO EXERCÍCIO:
{exercise_description}

═══════════════════════════════════════════════

CÓDIGO SUBMETIDO PELO ALUNO:
```python
{student_code}
```

═══════════════════════════════════════════════

Analise se o código do aluno:
1. Completa TODAS as tarefas pedidas no exercício
2. Produz a saída esperada (se exemplos foram fornecidos)
3. Está funcionalmente correto
4. Segue boas práticas básicas

Forneça feedback detalhado e educativo em JSON."""

            # Log antes de chamar API
            logging.info(f"📤 Enviando para OpenAI API (gpt-3.5-turbo)...")
            
            # Chama a API do OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=800,  # Aumentado para respostas mais detalhadas
                temperature=0.7
            )
            
            logging.info(f"📥 Resposta recebida da OpenAI")
            
            # Parse da resposta
            ai_response = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks se presente
            if ai_response.startswith('```'):
                ai_response = ai_response.split('```')[1]
                if ai_response.startswith('json'):
                    ai_response = ai_response[4:]
                ai_response = ai_response.strip()
            
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
                
                logging.info(f"✅ Correção IA concluída: score={result['score']}, correct={result['correct']}")
                return result
                
            except (json.JSONDecodeError, ValueError) as e:
                logging.error(f"Erro ao parsear resposta da IA: {e}")
                logging.error(f"Resposta recebida: {ai_response[:200]}")
                return self._fallback_response(student_code)
                
        except Exception as e:
            logging.error(f"Erro na correção automática: {e}")
            import traceback
            logging.error(traceback.format_exc())
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
        """Resposta de fallback quando a IA falha - com análise básica"""
        code_lines = [line.strip() for line in student_code.strip().split('\n') if line.strip()]
        code_lower = student_code.lower()
        
        # Análise básica do código
        has_print = 'print(' in code_lower
        has_input = 'input(' in code_lower
        has_variables = '=' in code_lower and not '==' in code_lower
        line_count = len(code_lines)
        
        # Gera feedback baseado no que detectou
        feedback_parts = []
        score = 50
        suggestions = []
        
        if line_count == 0:
            feedback_parts.append("Seu código está vazio.")
            suggestions.append("Comece escrevendo algum código Python")
            score = 0
        elif line_count < 3:
            feedback_parts.append("Seu código parece muito curto.")
            suggestions.append("Verifique se implementou tudo que foi pedido")
            score = 40
        else:
            feedback_parts.append("Você escreveu um código com várias linhas.")
            score = 60
        
        if has_print:
            feedback_parts.append("Detectei uso de print() - isso é bom!")
            score += 10
        else:
            suggestions.append("Use print() para exibir resultados")
        
        if has_variables:
            feedback_parts.append("Você está usando variáveis corretamente.")
            score += 10
        
        if has_input:
            feedback_parts.append("Seu código solicita entrada do usuário.")
            score += 5
        
        suggestions.append("Teste seu código manualmente para garantir que funciona")
        suggestions.append("Compare sua saída com os exemplos do exercício")
        
        feedback = " ".join(feedback_parts) + " Não foi possível uma análise completa automaticamente. Execute seu código e verifique se a saída está correta."
        
        return {
            "correct": None,  # Indica que não foi possível avaliar definitivamente
            "feedback": feedback,
            "score": min(score, 75),  # Máximo 75 em fallback
            "suggestions": suggestions[:3]
        }

# Instância global do corretor
corrector = AICorrector()