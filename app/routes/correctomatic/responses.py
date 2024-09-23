from flask import request, jsonify
from app.extensions import db
from app.models import Submission

from . import bp

# Endpoint to receive Correctomatic responses
@bp.route("/response", methods=["POST"])
def response():
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

