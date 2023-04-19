import flask
from flask import request

from . import db_session
from .users import User

blueprint = flask.Blueprint('recipess_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/...')
def get_recipes():
    pass