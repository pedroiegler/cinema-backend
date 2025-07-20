# Cinema Backend

Sistema de gerenciamento de cinema desenvolvido com Django e PostgreSQL.

## Configuração Inicial

### 1. Clonar o repositório
```bash
git clone <url-do-repo>
cd cinema-backend
```

### 2. Configurar variáveis de ambiente
```bash
# Copiar o arquivo de exemplo
cp dotenv_files/.env-example dotenv_files/.env

# Gerar uma nova SECRET_KEY
python scripts/generate_secret_key.py
```

Copie a SECRET_KEY gerada e substitua no arquivo `dotenv_files/.env`.

### 3. Executar com Docker
```bash
docker-compose up --build
```

## Estrutura do Projeto

- `project_cinema/` - Aplicação Django principal
- `movies/` - App para gerenciamento de filmes
- `scripts/` - Scripts utilitários
- `dotenv_files/` - Arquivos de configuração de ambiente