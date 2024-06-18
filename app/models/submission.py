from datetime import datetime, timezone
from ..extensions import db

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    started = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    status = db.Column(db.String(20), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    comments = db.Column(db.Text, nullable=True)
    errors = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(120), nullable=True)
