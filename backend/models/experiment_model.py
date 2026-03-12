# models/experiment_model.py
# Tracks a single experiment within a research project.

from database import db
from datetime import datetime, timezone


class Experiment(db.Model):
    __tablename__ = "experiments"

    id               = db.Column(db.Integer, primary_key=True)
    project_id       = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    title            = db.Column(db.String(255), nullable=False)
    hypothesis       = db.Column(db.Text, default="")
    method           = db.Column(db.Text, default="")   # methodology / procedure
    result           = db.Column(db.Text, default="")   # recorded outcome

    # Optional link to a paper that motivated this experiment
    related_paper_id = db.Column(db.Integer, db.ForeignKey("papers.id"), nullable=True)

    created_at       = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id":               self.id,
            "project_id":       self.project_id,
            "title":            self.title,
            "hypothesis":       self.hypothesis,
            "method":           self.method,
            "result":           self.result,
            "related_paper_id": self.related_paper_id,
            "created_at":       self.created_at.isoformat(),
        }
