# Sistema de Seeding de Dados Iniciais

Este projeto inclui um sistema automático para inserir dados iniciais no banco de dados durante a primeira inicialização do Docker.

## Como Funciona

1. **Primeira Execução**: Quando o container é iniciado pela primeira vez, o script `init_setup.sh` detecta que é a primeira execução e executa o seeding dos gêneros.

2. **Execuções Subsequentes**: Nas próximas inicializações, o sistema detecta que o setup já foi executado e pula o seeding.

3. **Controle de Estado**: Um arquivo `.setup_done` é criado no diretório do projeto para controlar se o setup já foi executado.

## Gêneros Inseridos Automaticamente

O sistema insere os seguintes gêneros:
- Ação
- Comédia  
- Drama
- Terror
- Ficção Científica
- Romance
- Thriller
- Aventura
- Animação
- Documentário
- Fantasia
- Musical
- Crime
- Guerra
- Western

## Comandos Django Disponíveis

### Inserir Gêneros Manualmente
```bash
docker exec -it project_cinema python manage.py seed_genres
```

### Resetar Setup (para desenvolvimento)
```bash
docker exec -it project_cinema python manage.py reset_setup
```

## Scripts Disponíveis

- `scripts/seed_data.sh`: Executa o seeding dos gêneros
- `scripts/init_setup.sh`: Controla a primeira inicialização
- `scripts/commands.sh`: Script principal que orquestra a inicialização

## Fluxo de Inicialização

1. `wait_psql.sh` - Aguarda o PostgreSQL estar disponível
2. `migrate.sh` - Executa as migrações do Django
3. `init_setup.sh` - Executa o setup inicial (apenas na primeira vez)
4. `runserver.sh` - Inicia o servidor Django

## Para Desenvolvedores

Se você quiser forçar uma nova execução do seeding:

1. Execute o comando reset:
   ```bash
   docker exec -it project_cinema python manage.py reset_setup
   ```

2. Reinicie o container:
   ```bash
   docker-compose restart project_cinema
   ```

Ou simplesmente execute o seeding manualmente:
```bash
docker exec -it project_cinema python manage.py seed_genres
```