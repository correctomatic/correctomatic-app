from . import bp
from flask import g, current_app, send_from_directory, redirect, url_for

from app.models import Submission
from .utils import require_launch_data

@bp.route('/download/<int:submission_id>')
@require_launch_data()
def download(submission_id):
    current_user = g.current_user
    submission = Submission.query.get_or_404(submission_id)

    if submission.user_id != current_user:
        return redirect(url_for('submissions.index'))

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], submission.filename, as_attachment=True)
