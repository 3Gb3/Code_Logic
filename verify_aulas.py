#!/usr/bin/env python3
"""
Script para verificar conceitos inadequados nas aulas
"""

import os
import re
from pathlib import Path

# Padrões proibidos
FORBIDDEN_PATTERNS = {
    'funcoes': r'\bdef\s+\w+\s*\(',
    'classes': r'\bclass\s+\w+',
    'imports': r'\b(import|from)\s+\w+',
    'lambda': r'\blambda\s+',
    'try_except': r'\btry\s*:',
    'list_comprehension': r'\[.+\s+for\s+.+\s+in\s+.+\]',
    'decorators': r'@\w+',
    'generators': r'\byield\s+',
    'dunder': r'\b__\w+__\b',
}

def verificar_arquivo(filepath):
    """Verifica um arquivo e retorna conceitos proibidos encontrados"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    problemas = []
    for conceito, pattern in FORBIDDEN_PATTERNS.items():
        matches = re.findall(pattern, content, re.MULTILINE)
        if matches:
            # Conta ocorrências únicas
            unique_matches = set(matches)
            problemas.append(f"  ❌ {conceito}: {len(matches)} ocorrências ({len(unique_matches)} únicas)")
    
    return problemas

def main():
    base_path = Path("/home/gbs/Downloads/Gb/Code_Logic/templates/exercicios")
    modulos = ['sequencial', 'comparativa', 'repetitiva', 'vetores', 'matrizes']
    
    total_problemas = 0
    arquivos_com_problemas = []
    
    print("=" * 80)
    print("VERIFICAÇÃO DE CONCEITOS INADEQUADOS NAS AULAS")
    print("=" * 80)
    print()
    
    for modulo in modulos:
        print(f"\n{'='*80}")
        print(f"📚 MÓDULO: {modulo.upper()}")
        print('='*80)
        
        modulo_path = base_path / modulo
        modulo_problemas = 0
        
        for i in range(1, 11):
            arquivo = modulo_path / f"aula{i}.html"
            if not arquivo.exists():
                print(f"  ⚠️  Aula {i}: Arquivo não encontrado")
                continue
            
            problemas = verificar_arquivo(arquivo)
            
            if problemas:
                print(f"\n  📄 Aula {i}:")
                for problema in problemas:
                    print(problema)
                modulo_problemas += len(problemas)
                total_problemas += len(problemas)
                arquivos_com_problemas.append(str(arquivo))
            else:
                print(f"  ✅ Aula {i}: OK")
        
        print(f"\n  📊 Total de problemas no módulo: {modulo_problemas}")
    
    print(f"\n\n{'='*80}")
    print(f"📊 RESUMO GERAL")
    print('='*80)
    print(f"Total de arquivos com problemas: {len(arquivos_com_problemas)}")
    print(f"Total de tipos de problemas encontrados: {total_problemas}")
    print()
    
    if arquivos_com_problemas:
        print("Arquivos que precisam de correção:")
        for arq in arquivos_com_problemas:
            print(f"  - {arq}")

if __name__ == "__main__":
    main()
