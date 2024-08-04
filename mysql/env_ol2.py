# alembic/env.py

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import sqlalchemy as sa
import datetime

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

database_url=config.get_main_option("sqlalchemy.url")

def create_alembic_log_table(connection):
    """Creates the alembic_log table if it doesn't exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS alembic_log (
        id SERIAL PRIMARY KEY,
        message TEXT NOT NULL,
        logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    connection.execute(sa.text(create_table_query))

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()
        

def log_migration(connection, context):
    """Logs each migration step to the alembic_log table"""
    current_revision = context.get_current_revision()
    target_revision = context.get_head_revision()
    direction = "upgrade" if target_revision != current_revision else "downgrade"
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    message = (f"Timestamp: {timestamp}\n"
            f"Performed {direction}\n"
            f"Current Revision: {current_revision}\n"
            f"Target Revision: {target_revision}\n")

    # Print the log message
    print(f"Log:{message}")

    # Insert the log message into the database
    connection.execute(
        sa.text("INSERT INTO alembic_log (message) VALUES (:message)"),
        {"message": message}
    )

def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    from sqlalchemy import create_engine

    connectable = create_engine(database_url)

    with connectable.connect() as connection:
        # Create the alembic_log table if it doesn't exist
        create_alembic_log_table(connection)
        
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=lambda ctx, rev, directives: log_migration(connection, ctx)
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
