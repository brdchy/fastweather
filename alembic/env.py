from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

# Импортируйте вашу базовую модель
from models import Base

# Этот шаг важен для настройки логгирования
fileConfig(context.config.config_file_name)

# Добавьте вашу базовую модель в контекст
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=context.config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    configuration = context.config.get_section(context.config.config_ini_section)
    configuration['sqlalchemy.url'] = context.config.get_main_option("sqlalchemy.url")
    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()