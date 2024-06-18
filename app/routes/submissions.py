from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory

from ..extensions import db
from ..models import Submission

bp = Blueprint('submissions', __name__)

def get_current_user():
    # Placeholder function. Replace with actual logic to get the current user.
    return "current_user"

def unique_filename(filename):
    unique_id = uuid.uuid4().hex
    filename = secure_filename(filename)
    return f"{unique_id}_{filename}"

# Define a custom Jinja2 filter
@current_app.template_filter('nl2br')
def nl2br(value):
    """Convert newlines to <br> tags."""
    return value.replace('\n', '<br>')

@bp.route('/submissions')
def index():
    current_user = get_current_user()
    submissions = (Submission.query
        .filter_by(user_id=current_user)
        .order_by(Submission.started.desc())
        .all()
        )
    last_submission = submissions[0] if submissions else None
    last_submission_pending = last_submission and last_submission.status == 'Pending'

    return render_template(
        'submissions.jinja2',
        submissions=submissions,
        last_submission_pending=last_submission_pending
        )

import requests
def banana(submission_id, filename):
    # Simulate the curl request internally
    payload = {
        'file': (filename, open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'rb')),
        'work_id': 'my-id-for-exercise 8888',
        'assignment_id': 'correction-test-1',
        'callback': 'http://host.docker.internal:3333/log' + '/correctomatic-response'
    }
    headers = {
        'User-Agent': 'insomnium/0.2.3-a',
    }
    response = requests.post('http://localhost:8080/grade', files=payload, headers=headers)

    # Check the response from the simulated request
    if response.status_code != 200:
        # Handle the error as needed
        return f"Error: {response.status_code} - {response.text}", 500

@bp.route('/new_submission', methods=['POST'])
def new_submission():
    current_user = get_current_user()

    # Check if the last submission is still pending
    last_submission = (
        Submission.query
          .filter_by(user_id=current_user)
          .order_by(Submission.started.desc()).first()
        )
    if last_submission and last_submission.status == 'Pending':
        return redirect(url_for('submissions.index'))

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = unique_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        new_entry = Submission(
            user_id=current_user,
            started=datetime.now(),
            status='Pending',
            comments='',
            errors='',
            filename=filename
        )
        db.session.add(new_entry)
        db.session.commit()

    return redirect(url_for('submissions.index'))

@bp.route('/download/<int:submission_id>')
def download_file(submission_id):
    current_user = get_current_user()
    submission = Submission.query.get_or_404(submission_id)

    if submission.user_id != current_user:
        return redirect(url_for('submissions.index'))

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], submission.filename, as_attachment=True)
