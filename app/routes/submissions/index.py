from flask import g, current_app, render_template
from . import bp

from app.models import Submission
from .utils import require_launch_data

# Define a custom Jinja2 filter
@current_app.template_filter('nl2br')
def nl2br(value):
    """Convert newlines to <br> tags."""
    if value is None:
        return ''
    return str(value).replace('\n', '<br>')

@bp.route('/', methods=["GET", "POST"])
@require_launch_data(methods=['GET', 'POST'])
def index():
    current_user = g.current_user
    assignment_id = g.assignment_id
    current_app.logger.info(f"Current user: {current_user}. Assignment ID: {assignment_id}")
    submissions = (Submission.query
        .filter_by(user_id=current_user)
        .order_by(Submission.started.desc())
        .all()
        )
    last_submission = submissions[0] if submissions else None
    last_submission_pending = last_submission and last_submission.status == 'Pending'

    return render_template(
        'submissions.html.j2',
        submissions=submissions,
        last_submission_pending=last_submission_pending,
        assignment_id=assignment_id
        )
