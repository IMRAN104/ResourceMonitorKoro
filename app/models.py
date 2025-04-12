from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ResourceMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpu_usage = db.Column(db.Float, nullable=False)
    memory_usage = db.Column(db.Float, nullable=False)
    disk_usage = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

class ProcessInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cpu_usage = db.Column(db.Float, nullable=False)
    memory_usage = db.Column(db.Float, nullable=False)
    is_resource_hungry = db.Column(db.Boolean, default=False)