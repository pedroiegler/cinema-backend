#!/bin/sh

set -e

# Arquivo de controle para verificar se já foi executado
# Usando /project_cinema para persistir entre reinicializações do container
SETUP_FLAG="/project_cinema/.setup_done"

echo "🚀 Verificando se é a primeira inicialização..."

if [ ! -f "$SETUP_FLAG" ]; then
    echo "📋 Primeira inicialização detectada - executando setup inicial..."
    
    # Executa o seeding dos dados
    ./seed_data.sh
    
    # Cria o arquivo de controle
    touch "$SETUP_FLAG"
    echo "✅ Setup inicial concluído!"
else
    echo "ℹ️  Setup inicial já foi executado anteriormente"
fi