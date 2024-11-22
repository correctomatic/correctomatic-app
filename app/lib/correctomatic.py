
import os
import requests
from flask import current_app, url_for

def send_correction_request(assignment_id, submission_id, filename, custom_params={}):
    current_app.logger.debug(f"Calling send_correction_request function with assignment_id={assignment_id}, submission_id={submission_id}, filename={filename}")

    callback_host = current_app.config['CALLBACK_HOST']
    upload_folder = current_app.config['UPLOAD_FOLDER']
    api_server = current_app.config['CORRECTOMATIC_API_SERVER']
    file_path = os.path.join(upload_folder, filename)

    if not os.path.exists(file_path):
        raise Exception(f"Error: File {file_path} does not exist")

    with open(file_path, 'rb') as file:
        # We need to send the file as a tuple because we have repeated param fields
        files = [
            ('file', (filename, file)),
            ('work_id', (None, submission_id)),
            ('assignment_id', (None, assignment_id)),
            ('callback', (None, f'{callback_host}{url_for("correctomatic.response")}'))
        ]

        # Add custom params to the request
        for key, value in custom_params.items():
            if key != 'assignment_id':  # Excluir 'assignment_id'
                files.append(('param', (None, f"{key}={value}")))

        current_app.logger.debug(f"Sending request to {api_server}/grade with files: {files}")
        response = requests.post(f'{api_server}/grade', files=files, timeout=5)

    if response.status_code != 200:
        raise Exception(f'Error: {response.status_code} - {response.text}')

    response_data = response.json()
    if not response_data.get("success"):
        raise Exception(f'Error: {response_data.get("message", "Unknown error occurred")}')

    return True
