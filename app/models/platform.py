from ..extensions import db

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)  # Not unique now, multiple entries allowed
    client_id = db.Column(db.String(255), nullable=False)
    auth_login_url = db.Column(db.String(255), nullable=False)
    auth_token_url = db.Column(db.String(255), nullable=False)
    auth_audience = db.Column(db.String(255), nullable=True)
    key_set_url = db.Column(db.String(255), nullable=False)
    private_key_file = db.Column(db.String(255), nullable=False)
    public_key_file = db.Column(db.String(255), nullable=False)
    default = db.Column(db.Boolean, default=False)

    deployments = db.relationship('Deployment', backref='platform', lazy=True)
