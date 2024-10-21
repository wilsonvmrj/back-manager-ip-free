### Alembic commands

### Gerando a o migration

alembic revision --autogenerate -m "Create users table"

### Subindo a migracao para o banco

alembic upgrade head
