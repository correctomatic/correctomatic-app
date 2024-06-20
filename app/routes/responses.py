from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Submission

bp = Blueprint("correctomatic", __name__)


# Endpoint to receive Correctomatic responses
@bp.route("/correctomatic-response", methods=["POST"])
def correctomatic_response():
    is_json = request.is_json
    if not is_json: return jsonify({"message": "Invalid JSON payload"}), 400
    
    data = request.get_json()

    # Extract relevant fields from the JSON payload
    success = data.get("success", False)
    work_id = data.get("work_id", "")
    grade = data.get("grade")
    comments = data.get("comments")
    error = data.get("error")

    # Find the corresponding submission record in the database
    submission = Submission.query.filter_by(id=work_id).first()

    if not submission : return jsonify({"message": "Submission not found"}), 404

    # Update the submission based on the response type (success or failure)
    if success:
        submission.status = "Completed"
        submission.grade = str(grade) if grade else None
        submission.comments = "\n".join(comments) if comments else None
    else:
        submission.status = "Failed"
        submission.errors = error

    # Commit changes to the database
    db.session.commit()

    return jsonify({"message": "Submission updated successfully"}), 200

