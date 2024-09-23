from flask import g, current_app, render_template, flash, abort
from werkzeug.exceptions import BadRequest

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

def check_required_params():
    if not g.current_user:
        raise BadRequest("Missing user in request")
    if not g.assignment_id:
        raise BadRequest("Missing assignment id in request. Please add 'assignment_id=your assignment id' as a parameter.")

@bp.route('/', methods=["GET"])
@require_launch_data()
def index():

    try:
        check_required_params()

        current_user = g.current_user
        assignment_id = g.assignment_id

        submissions = (Submission.query
            .filter_by(user_id=current_user, assignment_id=assignment_id)
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

    except BadRequest as e:
        current_app.logger.error(f"Failed to load submissions: {e}")
        flash(e.description, "error")
        abort(400)

    except Exception as e:
        current_app.logger.error(f"Failed to load submissions: {e}")
        flash("Failed to load submissions", "error")
        abort(500)
