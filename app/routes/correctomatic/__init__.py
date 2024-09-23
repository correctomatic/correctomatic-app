from flask import Blueprint

bp = Blueprint('correctomatic', __name__)

from .responses import response
