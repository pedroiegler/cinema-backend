# Documentação do Sistema Cinema Backend

## Visão Geral

O **Cinema Backend** é um sistema de gerenciamento de cinema desenvolvido com Django REST Framework e PostgreSQL. O sistema permite o gerenciamento completo de filmes, gêneros, avaliações e comentários, oferecendo uma API REST robusta para aplicações frontend.

## Arquitetura do Sistema

### Stack Tecnológica

- **Backend**: Django 4.2+ com Django REST Framework
- **Banco de Dados**: PostgreSQL 14
- **Containerização**: Docker e Docker Compose
- **Linguagem**: Python 3.11
- **Documentação da API**: Swagger/OpenAPI (drf-yasg)

### Estrutura do Projeto

```
cinema-backend/
├── project_cinema/           # Aplicação Django principal
│   ├── cinema/              # Configurações do projeto
│   │   ├── settings.py      # Configurações principais
│   │   ├── urls.py          # URLs principais
│   │   ├── wsgi.py          # WSGI configuration
│   │   └── asgi.py          # ASGI configuration
│   ├── movies/              # App de filmes
│   │   ├── models.py        # Modelos de dados
│   │   ├── views.py         # Views da API
│   │   ├── serializers.py   # Serializers DRF
│   │   ├── urls.py          # URLs do app
│   │   ├── admin.py         # Configuração do admin
│   │   └── migrations/      # Migrações do banco
│   ├── manage.py            # Comando Django
│   └── requirements.txt     # Dependências Python
├── scripts/                 # Scripts utilitários
├── dotenv_files/           # Arquivos de configuração
├── docker-compose.yml      # Configuração Docker
└── Dockerfile             # Imagem Docker
```

## Modelos de Dados

### 1. Genre (Gênero)
Representa os gêneros cinematográficos.

**Campos:**
- `id`: Identificador único
- `name`: Nome do gênero (único, max 100 caracteres)
- `description`: Descrição opcional

**Relacionamentos:**
- Relacionamento Many-to-Many com Movie

### 2. Movie (Filme)
Modelo principal que representa um filme.

**Campos:**
- `id`: Identificador único
- `title`: Título do filme (max 200 caracteres)
- `synopsis`: Sinopse do filme
- `duration`: Duração em minutos
- `release_date`: Data de lançamento
- `director`: Nome do diretor (max 200 caracteres)
- `cast`: Elenco principal
- `poster`: Imagem do poster (upload para 'posters/')
- `trailer_url`: URL do trailer (opcional)
- `is_active`: Status ativo/inativo
- `created_at`: Data de criação
- `updated_at`: Data de atualização

**Relacionamentos:**
- Many-to-Many com Genre
- One-to-Many com Rating
- One-to-Many com Comment

**Propriedades Calculadas:**
- `average_rating`: Média das avaliações
- `total_ratings`: Total de avaliações

### 3. Rating (Avaliação)
Representa as avaliações dos usuários para os filmes.

**Campos:**
- `id`: Identificador único
- `movie`: Referência ao filme
- `user`: Referência ao usuário
- `rating`: Nota de 1 a 5
- `created_at`: Data de criação
- `updated_at`: Data de atualização

**Restrições:**
- Unique constraint: um usuário só pode avaliar um filme uma vez
- Validação: rating deve ser entre 1 e 5

### 4. Comment (Comentário)
Representa os comentários dos usuários sobre os filmes.

**Campos:**
- `id`: Identificador único
- `movie`: Referência ao filme
- `user`: Referência ao usuário
- `content`: Conteúdo do comentário
- `is_active`: Status ativo/inativo
- `created_at`: Data de criação
- `updated_at`: Data de atualização

## API Endpoints

### Base URL
- Desenvolvimento: `http://localhost:8000/api/`
- Documentação Swagger: `http://localhost:8000/swagger/`
- Documentação ReDoc: `http://localhost:8000/redoc/`

### Endpoints Principais

#### Gêneros
- `GET /api/genres/` - Listar gêneros
- `POST /api/genres/` - Criar gênero
- `GET /api/genres/{id}/` - Detalhar gênero
- `PUT /api/genres/{id}/` - Atualizar gênero
- `DELETE /api/genres/{id}/` - Deletar gênero

**Filtros disponíveis:**
- Busca: `?search=acao`
- Ordenação: `?ordering=name`

#### Filmes
- `GET /api/movies/` - Listar filmes
- `POST /api/movies/` - Criar filme
- `GET /api/movies/{id}/` - Detalhar filme
- `PUT /api/movies/{id}/` - Atualizar filme
- `DELETE /api/movies/{id}/` - Deletar filme

**Endpoints especiais:**
- `GET /api/movies/top_rated/` - Top 10 filmes mais bem avaliados
- `GET /api/movies/recent/` - Top 10 filmes recentes
- `GET /api/movies/coming_soon/` - Top 10 filmes em breve
- `POST /api/movies/{id}/rate/` - Avaliar filme (requer autenticação)
- `DELETE /api/movies/{id}/remove_rating/` - Remover avaliação (requer autenticação)

**Filtros disponíveis:**
- Por gênero: `?genres=1,2`
- Por data: `?release_date=2024-01-01`
- Busca: `?search=batman`
- Ordenação: `?ordering=-release_date`

#### Avaliações
- `GET /api/ratings/` - Listar avaliações do usuário (requer autenticação)
- `POST /api/ratings/` - Criar avaliação (requer autenticação)
- `GET /api/ratings/{id}/` - Detalhar avaliação
- `PUT /api/ratings/{id}/` - Atualizar avaliação
- `DELETE /api/ratings/{id}/` - Deletar avaliação

#### Comentários
- `GET /api/comments/` - Listar comentários
- `POST /api/comments/` - Criar comentário (requer autenticação)
- `GET /api/comments/{id}/` - Detalhar comentário
- `PUT /api/comments/{id}/` - Atualizar comentário (apenas próprios)
- `DELETE /api/comments/{id}/` - Deletar comentário

**Filtros disponíveis:**
- Por filme: `?movie=1`
- Ordenação: `?ordering=-created_at`

## Serializers

### Estratégia de Serialização
O sistema utiliza diferentes serializers para diferentes contextos:

1. **MovieListSerializer**: Versão simplificada para listagens
2. **MovieDetailSerializer**: Versão completa com comentários
3. **MovieSerializer**: Versão padrão para CRUD

### Serializers Implementados

#### UserSerializer
Serializer para representação de usuários nas respostas da API.

**Campos incluídos:**
- `id`: Identificador único do usuário
- `username`: Nome de usuário
- `last_name`: Sobrenome do usuário

**Uso:** Utilizado como campo aninhado em RatingSerializer e CommentSerializer para mostrar informações básicas do usuário.

#### GenreSerializer
Serializer completo para gêneros cinematográficos.

#### RatingSerializer
Serializer para avaliações de filmes.
- Inclui informações do usuário via UserSerializer (read-only)
- Automaticamente associa o usuário autenticado na criação

#### CommentSerializer
Serializer para comentários de filmes.
- Inclui informações do usuário via UserSerializer (read-only)
- Automaticamente associa o usuário autenticado na criação

#### MovieSerializer
Serializer principal para filmes com funcionalidades avançadas:
- Relacionamento com gêneros (leitura e escrita)
- Campos calculados (average_rating, total_ratings)
- Campo user_rating que retorna a avaliação do usuário atual

### Campos Especiais
- `user_rating`: Retorna a avaliação do usuário atual
- `average_rating`: Média calculada das avaliações
- `total_ratings`: Total de avaliações
- `comments_count`: Total de comentários ativos

## Configurações

### Variáveis de Ambiente
O sistema utiliza arquivo `.env` em `dotenv_files/.env`:

```env
# Django
SECRET_KEY=sua-secret-key-aqui
DEBUG=0
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=cinema_db
POSTGRES_USER=cinema_user
POSTGRES_PASSWORD=cinema_password
POSTGRES_HOST=psql
POSTGRES_PORT=5432

# Email (opcional)
CONTACT_EMAIL=admin@cinema.com
```

### Configurações Django
- **Timezone**: America/Sao_Paulo
- **Language**: pt-br
- **CORS**: Habilitado para todos os origins (desenvolvimento)
- **Media Files**: Upload em `/media/`
- **Static Files**: Servidos em `/static/`

## Funcionalidades Implementadas

### 1. Gerenciamento de Filmes
- ✅ CRUD completo de filmes
- ✅ Upload de posters
- ✅ Relacionamento com gêneros
- ✅ Status ativo/inativo
- ✅ Filtros e busca avançada
- ✅ Ordenação por diferentes campos

### 2. Sistema de Avaliações
- ✅ Avaliação de 1 a 5 estrelas
- ✅ Uma avaliação por usuário por filme
- ✅ Cálculo automático de média
- ✅ Endpoint para top filmes avaliados

### 3. Sistema de Comentários
- ✅ Comentários por filme
- ✅ Moderação (is_active)
- ✅ Edição apenas de próprios comentários
- ✅ Filtros por filme

### 4. Categorização
- ✅ Gêneros cinematográficos
- ✅ Relacionamento Many-to-Many com filmes
- ✅ Filtros por gênero

### 5. Endpoints Especiais
- ✅ Filmes recentes
- ✅ Filmes em breve
- ✅ Top filmes avaliados
- ✅ Avaliação rápida via endpoint

### 6. Documentação
- ✅ Swagger UI integrado
- ✅ ReDoc integrado
- ✅ Documentação automática da API

## Segurança e Permissões

### Autenticação
- Sistema baseado em sessões Django
- Endpoints públicos: listagem e detalhes
- Endpoints privados: avaliações e comentários

### Permissões Implementadas
- **Comentários**: Criação requer autenticação, edição apenas próprios
- **Avaliações**: Operações requerem autenticação (controlado a nível de queryset)
- **Filmes**: Leitura pública, ações de avaliação requerem autenticação
- **Gêneros**: Leitura pública, escrita requer autenticação (admin)

### Controle de Acesso
- **RatingViewSet**: Acesso restrito ao usuário através de `get_queryset()` que filtra por `user=self.request.user`, com tratamento especial para geração de schema Swagger e usuários não autenticados
- **CommentViewSet**: Validação de propriedade implementada em `perform_update()` para edição de comentários
- **MovieViewSet**: Ações de avaliação (`rate`, `remove_rating`) requerem usuário autenticado

## Infraestrutura

### Docker
O sistema é completamente containerizado:

**Serviços:**
- `project_cinema`: Aplicação Django (porta 8000)
- `psql`: PostgreSQL 14 (porta 5433 externa)

**Volumes:**
- `postgres_data`: Persistência do banco de dados
- Bind mount: `./project_cinema:/project_cinema` (desenvolvimento)

### Scripts de Inicialização

O sistema utiliza uma sequência ordenada de scripts para garantir inicialização correta:

1. **`wait_psql.sh`**: Aguarda PostgreSQL estar disponível
2. **`migrate.sh`**: Executa migrações do banco de dados
3. **`runserver.sh`**: Inicia o servidor Django

#### Fluxo de Inicialização Detalhado

O script principal `commands.sh` orquestra toda a inicialização:

```bash
wait_psql.sh    # Aguarda banco estar pronto
migrate.sh      # Aplica migrações
runserver.sh    # Inicia servidor
```

#### Sistema de Seeding Manual

O sistema não executa mais seeding automático durante a inicialização. Os dados iniciais devem ser inseridos manualmente quando necessário.

**Scripts do Sistema de Seeding:**
- `scripts/seed_data.sh`: Executa o comando Django `seed_genres` (execução manual)
- `scripts/commands.sh`: Orquestra o fluxo de inicialização básico

### Comandos Django Personalizados

#### seed_genres
Comando para popular o banco de dados com gêneros cinematográficos iniciais.

**Localização**: `project_cinema/movies/management/commands/seed_genres.py`

**Uso**:
```bash
python manage.py seed_genres
```

**Funcionalidades**:
- Insere 15 gêneros cinematográficos pré-definidos
- Utiliza `get_or_create()` para evitar duplicatas
- Fornece feedback detalhado sobre o processo
- Exibe resumo com estatísticas de criação

**Gêneros incluídos**:
- Ação, Comédia, Drama, Terror, Ficção Científica
- Romance, Thriller, Aventura, Animação, Documentário
- Fantasia, Musical, Crime, Guerra, Western

**Saída do comando**:
- ✓ Confirmação para cada gênero criado
- ⚠ Aviso para gêneros já existentes
- 📊 Resumo final com estatísticas

## Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados
- Git

### Passos para Execução

1. **Clonar o repositório**
```bash
git clone <url-do-repo>
cd cinema-backend
```

2. **Configurar variáveis de ambiente**
```bash
# Copiar arquivo de exemplo
cp dotenv_files/.env-example dotenv_files/.env

# Gerar SECRET_KEY
python scripts/.py/generate_secret_key.py
```

3. **Executar com Docker**
```bash
docker-compose up --build
```

4. **Acessar a aplicação**
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Swagger: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Dependências Python

### Principais
- **Django 4.2+**: Framework web
- **djangorestframework**: API REST
- **psycopg2-binary**: Driver PostgreSQL
- **django-cors-headers**: CORS
- **python-dotenv**: Variáveis de ambiente
- **drf-yasg**: Documentação Swagger
- **django-filter**: Filtros avançados
- **Pillow**: Processamento de imagens

## Status do Desenvolvimento

### ✅ Implementado
- Modelos de dados completos
- API REST funcional
- Sistema de avaliações
- Sistema de comentários
- Filtros e busca
- Documentação automática
- Containerização
- Scripts de deploy

### 🔄 Possíveis Melhorias Futuras
- Sistema de autenticação JWT
- Cache com Redis
- Testes automatizados
- CI/CD pipeline
- Logs estruturados
- Monitoramento
- Rate limiting
- Paginação otimizada
- Notificações
- Sistema de favoritos

## Considerações Técnicas

### Performance
- Queries otimizadas com select_related/prefetch_related
- Índices automáticos em ForeignKeys
- Paginação padrão do DRF

### Escalabilidade
- Arquitetura preparada para múltiplas instâncias
- Banco de dados separado em container
- Media files configurados para storage externo

### Manutenibilidade
- Código organizado em apps Django
- Serializers específicos por contexto
- Configurações centralizadas
- Scripts automatizados

## Correções Recentes

### 26/07/2025 - Correção do Caminho do Script de Geração de SECRET_KEY

**Mudança Implementada:**
- Corrigido o caminho do script de geração de SECRET_KEY no README.md
- Caminho atualizado de `python scripts/generate_secret_key.py` para `python scripts/.py/generate_secret_key.py`

**Motivação:**
- Alinhar a documentação com a estrutura real de diretórios do projeto
- Scripts Python estão organizados no subdiretório `scripts/.py/`
- Garantir que os comandos de configuração inicial funcionem corretamente

**Impacto:**
- ✅ **Comandos de setup funcionam**: Usuários conseguem gerar a SECRET_KEY corretamente
- ✅ **Documentação alinhada**: README.md reflete a estrutura real do projeto
- ✅ **Experiência do desenvolvedor**: Processo de configuração inicial sem erros

**Arquivos Afetados:**
- `README.md`: Comando de geração de SECRET_KEY corrigido

### 26/07/2025 - Correção do Comando de Inicialização do Container

**Mudança Implementada:**
- Corrigido o comando CMD no Dockerfile de `[".sh/commands.sh"]` para `["/scripts/.sh/commands.sh"]`
- Comando agora referencia corretamente o caminho absoluto completo do script

**Motivação:**
- Corrigir erro de execução onde o container não conseguia localizar o script `commands.sh`
- Garantir que o script de inicialização seja encontrado independentemente do diretório de trabalho
- Usar caminho absoluto para maior confiabilidade na execução

**Impacto:**
- ✅ **Container inicia corretamente**: Script de inicialização é encontrado e executado
- ✅ **Caminho absoluto confiável**: Não depende de PATH ou diretório atual
- ✅ **Estrutura de diretórios respeitada**: Comando reflete a organização real dos scripts

**Detalhes Técnicos:**
- Scripts estão organizados em `scripts/.sh/` no container
- CMD usa caminho absoluto: `/scripts/.sh/commands.sh`
- Estrutura mantém organização por tipo de arquivo (.sh, .py)

**Arquivos Afetados:**
- `Dockerfile`: Linha CMD corrigida para usar caminho absoluto

### 26/07/2025 - Simplificação do Sistema de Inicialização

**Mudança Implementada:**
- Removido o script `init_setup.sh` da sequência de inicialização automática
- Sistema de seeding automático desabilitado durante o startup do container
- Inicialização agora segue fluxo mais simples e direto

**Motivação:**
- Simplificar o processo de inicialização do container
- Dar maior controle ao desenvolvedor sobre quando executar o seeding
- Reduzir complexidade e possíveis pontos de falha no startup

**Impacto:**
- ⚠️ **Seeding não é mais automático**: Gêneros devem ser inseridos manualmente
- ✅ **Inicialização mais rápida**: Menos etapas no processo de startup
- ✅ **Maior controle**: Desenvolvedor decide quando popular dados iniciais
- ✅ **Menos complexidade**: Fluxo de inicialização mais direto

**Como Popular Dados Iniciais Agora:**
```bash
# Executar manualmente após o container estar rodando
docker exec -it project_cinema python manage.py seed_genres
```

**Arquivos Afetados:**
- `scripts/commands.sh`: Removida linha `init_setup.sh`

### 20/07/2025 - Correção Crítica no Sistema de Inicialização

**Problema Identificado:**
- O script `scripts/init_setup.sh` estava com sintaxe incorreta devido à ausência do comando `fi` para fechar o bloco condicional
- Esta falha impediria a execução correta do sistema de inicialização automática

**Correção Aplicada:**
- Restaurado o comando `fi` no final do bloco if-else
- Script agora executa corretamente o fluxo de inicialização
- Sistema de seeding automático funcionando conforme especificado

**Impacto:**
- ✅ Sistema de inicialização restaurado
- ✅ Seeding automático de gêneros funcionando
- ✅ Detecção de primeira execução operacional
- ✅ Arquivo de controle `.setup_done` sendo criado corretamente

**Arquivos Afetados:**
- `scripts/init_setup.sh`: Sintaxe corrigida

---

**Última atualização**: 20/07/2025
**Versão do Django**: 4.2+
**Versão do Python**: 3.11
**Versão do PostgreSQL**: 14