#!/bin/sh

set -e

echo "🌱 Iniciando seeding dos dados iniciais..."

# Executa o comando para inserir os gêneros
python manage.py seed_genres

echo "✅ Seeding concluído com sucesso!"