

import logging

import pytest
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from app import flask_app
from app.plugins import db
# flake8: noqa
from app.repositories.models import Ingredient, Order, IngredientDetail, Size

from seed import seeder

logging.basicConfig(level=logging.DEBUG)

manager = FlaskGroup(flask_app)

migrate = Migrate()
migrate.init_app(flask_app, db)


@manager.command('test', with_appcontext=False)
def test():
    return pytest.main(['-v', './app/test'])

@manager.command('seed', with_appcontext=True)
def seed():
    return seeder.seed()

@manager.command('drop', with_appcontext=True)
def drop():
    return seeder.drop()
if __name__ == '__main__':
    manager()
