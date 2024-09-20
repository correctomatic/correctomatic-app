import os
import requests
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app, redirect, request, g, url_for

from app.models import Submission
from app.extensions import db
from . import bp
from .utils import require_launch_data

def unique_filename(filename):
    unique_id = uuid.uuid4().hex
    filename = secure_filename(filename)
    return f"{unique_id}_{filename}"

def send_correction_request(assignment_id, submission_id, filename):
    current_app.logger.debug(f"Calling send_correction_request function with assignment_id={assignment_id}, submission_id={submission_id}, filename={filename}")

    callback_host = current_app.config['CALLBACK_HOST']
    upload_folder = current_app.config['UPLOAD_FOLDER']
    api_server = current_app.config['CORRECTOMATIC_API_SERVER']
    file_path = os.path.join(upload_folder, filename)

    # Ensure the file exists before making the request
    if not os.path.exists(file_path):
        return f"Error: File {filename} does not exist", 400

    with open(file_path, 'rb') as file:
        files = {
            'file': (filename, file),
        }
        data = {
            'work_id': submission_id,
            'assignment_id': assignment_id,
            'callback': f'{callback_host}/correctomatic-response'
        }

        current_app.logger.debug(f"Sending request to {api_server}/grade with data: {data}")
        response = requests.post(f'{api_server}/grade', files=files, data=data, timeout=5)

    # Check the response from the request
    if response.status_code != 200:
        # Handle the error as needed
        raise f'Error: {response.status_code} - {response.text}'

    response_data = response.json()
    if not response_data.get("success"):
        raise f'error: {response_data.get("message", "Unknown error occurred")}'

    return True

@bp.route('/new', methods=['POST'])
@require_launch_data()
def new():
    current_user = g.current_user

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

        assignment_id = request.form['assignment_id']
        send_correction_request(assignment_id, new_entry.id, filename)

    except Exception as e:
        # If banana fails, log the error (optional) and delete the entry
        db.session.delete(new_entry)
        db.session.commit()

        current_app.logger.debug(f"Error sending correction to correctomatic: {e}")
        # Remove the file. Todo: nested try/except
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        # Return an error message to the user
        return "An error occurred during submission. Please try again later.", 500

    current_app.logger.info(f"New submission: {new_entry}")
    return redirect(url_for('submissions.index'))

