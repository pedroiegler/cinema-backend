#!/usr/bin/env python3
"""
Script para gerar uma nova SECRET_KEY do Django
"""
import os
import sys

# Adiciona o diretório do projeto ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'project_cinema'))

try:
    from django.core.management.utils import get_random_secret_key
    secret_key = get_random_secret_key()
    print(f"Nova SECRET_KEY gerada:")
    print(f'SECRET_KEY="{secret_key}"')
    print("\nCopie e cole no seu arquivo .env")
except ImportError:
    print("Django não encontrado. Instale com: pip install django")