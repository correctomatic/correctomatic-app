from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, current_app

from ..extensions import db
from ..models import Submission

bp = Blueprint('submissions', __name__)

@bp.route('/submissions')
def submissions():
    submissions = Submission.query.all()
    return render_template('submissions.html', submissions=submissions)

def unique_filename(filename):
    unique_id = uuid.uuid4().hex
    filename = secure_filename(filename)
    return f"{unique_id}_{filename}"

@bp.route('/new_submission', methods=['POST'])
def new_submission():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = unique_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        new_entry = Submission(
            started=datetime.now(),
            status='Pending',
            comments='',
            errors='',
            filename=filename
        )
        db.session.add(new_entry)
        db.session.commit()

    return redirect(url_for('submissions.submissions'))
