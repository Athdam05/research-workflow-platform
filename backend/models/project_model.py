# models/project_model.py
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Represents a top-level research project workspace.

from database import db
from datetime import datetime, timezone


class Project(db.Model):
    __tablename__ = "projects"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, default="")
    created_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Cascade-delete child records when a project is removed
    papers      = db.relationship("Paper",      backref="project", cascade="all, delete-orphan", lazy=True)
    experiments = db.relationship("Experiment", backref="project", cascade="all, delete-orphan", lazy=True)
    insights    = db.relationship("Insight",    backref="project", cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        return {
            "id":          self.id,
            "title":       self.title,
            "description": self.description,
            "created_at":  self.created_at.isoformat(),
            # Quick counts so the UI doesn't need extra calls
            "paper_count":      len(self.papers),
            "experiment_count": len(self.experiments),
            "insight_count":    len(self.insights),
        }
