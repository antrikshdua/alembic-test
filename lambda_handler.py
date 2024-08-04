import json
import sys
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
    history = []
    for rev in script.walk_revisions(base='base', head='heads'):
        create_date = rev.log_entry.splitlines()[-1].lstrip()
        history.append({
            "Revision ID": rev.revision,
            "Revises": rev.down_revision,
            "Create Date": create_date,
            "Branch labels": rev.branch_labels,
            "Message": rev.doc
        })
    return history

def lambda_handler(event, context):
    command = event.get('command')
    response = {}

    if command == "upgrade":
        revision = event.get('revision', 'head')
        upgrade(revision)
        response = {"message": f"Upgraded to revision {revision}"}
    elif command == "downgrade":
        revision = event.get('revision', '-1')
        downgrade(revision)
        response = {"message": f"Downgraded to revision {revision}"}
    elif command == "revision":
        message = event.get('message', 'New revision')
        create_revision(message)
        response = {"message": f"Created new revision with message: {message}"}
    elif command == "history":
        show_history()
        response = {"message": "Displayed migration history"}
    elif command == "vhistory":
        history = show_verbose_history()
        response = {"verbose_history": history}
    else:
        response = {"error": "Invalid command"}
    
    print(dict(response))
    # return {
    #     'statusCode': 200,
    #     'body': response
    # }

if __name__ == "__main__":
    # For local testing
    test_event = {
        "command": "upgrade",
        "revision": "head"
    }
    # test_event = {
    #     "command": "downgrade",
    #     "revision": "-1"
    # }
    
    # {
    #     "command": "revision",
    #     "message": "Add new table"
    # }
    
    # {
    #     "command": "history"
    # }
    
    # test_event = {
    #     "command": "vhistory"
    # }
    print(lambda_handler(test_event, None))
