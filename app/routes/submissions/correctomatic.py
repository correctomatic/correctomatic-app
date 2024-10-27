
import os
import requests
from flask import current_app, url_for

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
            'callback': f'{callback_host}{url_for("correctomatic.response")}'
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
