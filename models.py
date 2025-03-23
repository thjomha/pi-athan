from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Times(db.Model):
    __tablename__ = 'times'  # Make sure this matches the existing table name

    # Composite primary key: Month and Day
    Month = db.Column(db.Integer, primary_key=True)
    Day = db.Column(db.Integer, primary_key=True)
    Fajr = db.Column(db.String(10), nullable=False)
    Sunrise = db.Column(db.String(10), nullable=False)
    Dhuhr = db.Column(db.String(10), nullable=False)
    Asr = db.Column(db.String(10), nullable=False)
    Magrib = db.Column(db.String(10), nullable=False)
    Isha = db.Column(db.String(10), nullable=False)
