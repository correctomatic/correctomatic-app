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
def banana(assignment_id, submission_id, filename):

    print(f"Calling banana function with assignment_id={assignment_id}, submission_id={submission_id}, filename={filename}")

    callback_host = current_app.config['CALLBACK_HOST']
    # Simulate the curl request internally
    payload = {
        'file': (filename, open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'rb')),
        'work_id': submission_id,
        'assignment_id': assignment_id, # 'correction-test-1',
        'callback': f'{callback_host}' + '/correctomatic-response'
    }

    # This is not working:
    # api-1                       | [11:55:27.141] DEBUG (1): Job data: work_id=undefined, assignment_id=undefined, callback=undefined

    response = requests.post('http://localhost:8080/grade', files=payload)

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
    if last_submission and last_submission.status == 'Pending' and False:
        return redirect(url_for('submissions.index'))

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']


    if file.filename == '':
        return redirect(request.url)

    if not file:
        return redirect(request.url)

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

    try:
        # Need to commit the transaction before calling the function
        # to get the new entry ID
        db.session.commit()

        banana('correction-test-1', new_entry.id, filename)

    except Exception as e:
        # If banana fails, log the error (optional) and roll back the transaction
        db.session.delete(new_entry)
        # Log the error or handle it as needed
        print(f"Error calling banana function: {e}")
        # Optionally, delete the uploaded file
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        # Return an error message to the user
        return "An error occurred during submission. Please try again later.", 500

    return redirect(url_for('submissions.index'))

@bp.route('/download/<int:submission_id>')
def download_file(submission_id):
    current_user = get_current_user()
    submission = Submission.query.get_or_404(submission_id)

    if submission.user_id != current_user:
        return redirect(url_for('submissions.index'))

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], submission.filename, as_attachment=True)
