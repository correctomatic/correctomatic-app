from flask import Blueprint

bp = Blueprint('submissions', __name__)

from .index import index
from .new import new
from .download import download
