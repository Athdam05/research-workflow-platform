# models/paper_model.py
# Represents an uploaded or linked research paper inside a project.

from database import db
from datetime import datetime, timezone


class Paper(db.Model):
    __tablename__ = "papers"

    id         = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    title      = db.Column(db.String(255), nullable=False)
    file_path  = db.Column(db.String(512), default=None)   # local path after upload
    link       = db.Column(db.String(1024), default=None)  # external URL

    # Stored as a comma-separated string for simplicity; parse on the client
    tags       = db.Column(db.Text, default="")

    # AI-ready fields — populated externally or via future AI pipeline
    summary    = db.Column(db.Text, default="")             # AI-generated summary
    keywords   = db.Column(db.Text, default="")             # AI-extracted keywords (comma-sep)
    concepts   = db.Column(db.Text, default="")             # AI-extracted concepts (comma-sep)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id":         self.id,
            "project_id": self.project_id,
            "title":      self.title,
            "file_path":  self.file_path,
            "link":       self.link,
            "tags":       self.tags.split(",") if self.tags else [],
            "summary":    self.summary,
            "keywords":   self.keywords.split(",") if self.keywords else [],
            "concepts":   self.concepts.split(",") if self.concepts else [],
            "created_at": self.created_at.isoformat(),
        }
