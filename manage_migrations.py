import sys
import argparse
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory

def get_alembic_config():
    alembic_cfg = Config("alembic.ini")
    return alembic_cfg

def upgrade(revision):
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, revision)

def downgrade(revision):
    alembic_cfg = get_alembic_config()
    command.downgrade(alembic_cfg, revision)

def create_revision(message):
    alembic_cfg = get_alembic_config()
    command.revision(alembic_cfg, message=message, autogenerate=True)

def show_history():
    alembic_cfg = get_alembic_config()
    command.history(alembic_cfg)

def show_verbose_history():
    alembic_cfg = get_alembic_config()
    script = ScriptDirectory.from_config(alembic_cfg)
    for rev in script.walk_revisions(base='base', head='heads'):
        create_date = rev.log_entry.splitlines()[-1].lstrip()
        print(f"Revision ID: {rev.revision}")
        print(f"Revises: {rev.down_revision}")
        print(f"{create_date}")
        print(f"Branch labels: {rev.branch_labels}")
        print(f"Message: {rev.doc}")
        print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="Manage Alembic Migrations")
    subparsers = parser.add_subparsers(dest="command")

    parser_upgrade = subparsers.add_parser("upgrade")
    parser_upgrade.add_argument("revision", type=str, help="Revision to upgrade to")

    parser_downgrade = subparsers.add_parser("downgrade")
    parser_downgrade.add_argument("revision", type=str, help="Revision to downgrade to")

    parser_revision = subparsers.add_parser("revision")
    parser_revision.add_argument("message", type=str, help="Message for the new revision")

    parser_history = subparsers.add_parser("history", help="Show migration history")

    parser_verbose_history = subparsers.add_parser("vhistory", help="Show detailed migration history")

    args = parser.parse_args()

    if args.command == "upgrade":
        upgrade(args.revision)
    elif args.command == "downgrade":
        downgrade(args.revision)
    elif args.command == "revision":
        create_revision(args.message)
    elif args.command == "history":
        show_history()
    elif args.command == "vhistory":
        show_verbose_history()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
