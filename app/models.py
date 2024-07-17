from app import db

class CompanyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    sub_category = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)

class SimulationConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config_name = db.Column(db.String(255), nullable=False)
    rules = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
