from ..extensions import db

class Deployment(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('platform_id', 'deployment_id'),
    )

    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'), nullable=False)
    deployment_id = db.Column(db.String(255), nullable=False)

    # Don't need to define the relationship, this model is only for creating the LTI configuraiton
    # platform = db.relationship('Platform', backref=db.backref('deployments', lazy=True))
