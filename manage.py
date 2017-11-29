import os
import sys

from flask.cli import with_appcontext

from flask_pw import BaseSignalModel
import click

from app import create_app, db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.config['SECRET_KEY'] = os.urandom(24)

@db.cli.command('createtables', short_help='Create database tables.')
@click.option('--safe', default=False, is_flag=True,
              help=('Check first whether the table exists '
                    'before attempting to create it.'))
@click.argument('models', nargs=-1, type=click.UNPROCESSED)
@with_appcontext
def create_tables(models, safe):
    from importlib import import_module
    from flask.globals import _app_ctx_stack
    app = _app_ctx_stack.top.app
    if models:
        pw_models = []

        module = import_module(app.config['PEEWEE_MODELS_MODULE'])
        for mod in models:
            model = getattr(module, mod)
            if not isinstance(model, BaseSignalModel):
                continue
            pw_models.append(model)
        if pw_models:
            db.database.create_tables(pw_models, safe)
        return
    db.database.create_tables(db.models, safe)

