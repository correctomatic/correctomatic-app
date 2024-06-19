from flask import Blueprint, redirect, url_for

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return redirect(url_for('submissions.index'))
