from flask import Blueprint

bounty = Blueprint('bounty', __name__)

from . import views
