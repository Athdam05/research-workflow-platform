# database.py
# Initializes SQLAlchemy and creates all tables.
#
# IMPORTANT: All models must be imported in app.py BEFORE init_db() is called
# so that SQLAlchemy metadata is fully populated before create_all() runs.

from flask_sqlalchemy import SQLAlchemy

# Single shared db instance imported by every model and route
db = SQLAlchemy()


def init_db(app):
    """
    Bind the SQLAlchemy instance to the Flask app and create all tables.
    Models are registered via imports at the top of app.py — do not re-import here.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("✅  Database tables created (or already exist).")
