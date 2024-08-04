# from alembic import context
# from sqlalchemy import engine_from_config, pool
# from logging.config import fileConfig
# import sqlalchemy as sa
# from datetime import datetime

# # this is the Alembic Config object, which provides
# # access to the values within the .ini file in use.
# config = context.config

# # Interpret the config file for Python logging.
# # This line sets up loggers basically.
# fileConfig(config.config_file_name)

# # add your model's MetaData object here
# # for 'autogenerate' support
# # from myapp import mymodel
# # target_metadata = mymodel.Base.metadata
# target_metadata = None

# database_url = config.get_main_option("sqlalchemy.url")

# def create_alembic_log_table(connection):
#     """Creates the alembic_log table if it doesn't exist."""
#     create_table_query = """
#     CREATE TABLE IF NOT EXISTS alembic_log (
#         id SERIAL PRIMARY KEY,
#         message TEXT NOT NULL,
#         logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     );
#     """
#     connection.execute(sa.text(create_table_query))

# def log_migration(connection, message):
#     """Logs each migration step to the alembic_log table"""
#     timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
#     full_message = f"{timestamp} - {message}"

#     # Print the log message
#     print(full_message)

#     # Insert the log message into the database
#     connection.execute(
#         sa.text("INSERT INTO alembic_log (message) VALUES (:message)"),
#         {"message": full_message}
#     )

# def process_revision_directives(context, revision, directives):
#     """Hook to log migration steps."""
#     connection = context.bind
#     if context.is_transactional_ddl():
#         with context.begin_transaction():
#             log_migration(connection, f"Running migration {revision}")

# # def run_migrations_offline():
# #     """Run migrations in 'offline' mode."""
# #     url = config.get_main_option("sqlalchemy.url")
# #     context.configure(
# #         url=url, target_metadata=target_metadata, literal_binds=True
# #     )

# #     with context.begin_transaction():
# #         context.run_migrations()

# def run_migrations_online():
#     """Run migrations in 'online' mode."""

#     from sqlalchemy import create_engine

#     connectable = create_engine(database_url)

#     with connectable.connect() as connection:
#         # Create the alembic_log table if it doesn't exist
#         create_alembic_log_table(connection)

#         context.configure(
#             connection=connection,
#             target_metadata=target_metadata,
#             process_revision_directives=process_revision_directives
#         )

#         with context.begin_transaction():
#             context.run_migrations()

# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()



from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import sqlalchemy as sa
from datetime import datetime

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

database_url = config.get_main_option("sqlalchemy.url")

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

def log_migration(connection, message):
    """Logs each migration step to the alembic_log table"""
    print("Log migration called")
    
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    full_message = f"{timestamp} - {message}"

    # Print the log message
    print(full_message)

    # Insert the log message into the database
    connection.execute(
        sa.text("INSERT INTO alembic_log (message) VALUES (:message)"),
        {"message": full_message}
    )

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""

    from sqlalchemy import create_engine

    connectable = create_engine(database_url)

    with connectable.connect() as connection:
        # Create the alembic_log table if it doesn't exist
        create_alembic_log_table(connection)

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

def process_revision_directives(context, revision, directives):
    print(directives)
    """Hook to log migration steps."""
    connection = context.bind
    for directive in directives:
        if hasattr(directive, 'upgrade_ops'):
            print("Enter up")
            log_migration(connection, f"Applying migration {directive.upgrade_ops.head}")
        elif hasattr(directive, 'downgrade_ops'):
            print("Enter down")
            
            log_migration(connection, f"Reverting migration {directive.downgrade_ops.head}")

if context.is_offline_mode():
    run_migrations_online()
else:
    run_migrations_online()
