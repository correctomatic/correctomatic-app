from flask import Blueprint, render_template

bp = Blueprint('home', __name__)

@bp.route('/home')
def index():
    return render_template('index.html')
