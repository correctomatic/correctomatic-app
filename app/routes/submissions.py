from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename
from flask import (
    Blueprint, render_template,
    request, redirect, url_for,
    current_app, send_from_directory,
    session
)

from ..extensions import db
from ..models import Submission

from ..lti_lib import (
    lti_tool_conf,
    lti_launch_data_storage,
    lti_config_dir
)
from pylti1p3.contrib.flask import (
    FlaskOIDCLogin,
    FlaskMessageLaunch,
    FlaskRequest,
    FlaskCacheDataStorage,
)

bp = Blueprint('submissions', __name__)

def unique_filename(filename):
    unique_id = uuid.uuid4().hex
    filename = secure_filename(filename)
    return f"{unique_id}_{filename}"

# Define a custom Jinja2 filter
@current_app.template_filter('nl2br')
def nl2br(value):
    """Convert newlines to <br> tags."""
    if value is None:
        return ''
    return str(value).replace('\n', '<br>')

def get_current_user():

    tool_conf = lti_tool_conf()
    flask_request = FlaskRequest()
    # launch_data_storage = lti_launch_data_storage()

    launch_id = session.get('launch_id')
    current_app.logger.debug(f'launch_id in submissions: {launch_id}')

    message_launch = FlaskMessageLaunch.from_cache(
        launch_id, flask_request, tool_conf,
        # launch_data_storage=launch_data_storage
    )
    data = message_launch.get_launch_data()
    current_app.logger.debug(data)
    return data.get("sub")

    # Placeholder function. Replace with actual logic to get the current user.
    return "current_user"


@bp.route('/submissions', methods=["GET", "POST"])
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
        last_submission_pending=last_submission_pending,
        container=current_app.config['DEFAULT_CONTAINER']
        )

import requests
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

        container = request.form['container']
        send_correction_request(container, new_entry.id, filename)

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

@bp.route('/download/<int:submission_id>')
def download_file(submission_id):
    current_user = get_current_user()
    submission = Submission.query.get_or_404(submission_id)

    if submission.user_id != current_user:
        return redirect(url_for('submissions.index'))

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], submission.filename, as_attachment=True)
