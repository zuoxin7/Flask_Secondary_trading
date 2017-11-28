from flask import Blueprint

goodsissue = Blueprint('goodsissue', __name__)

from . import views
