# models/insight_model.py
# A research insight or note that can be tied to a paper and/or experiment.

from database import db
from datetime import datetime, timezone


class Insight(db.Model):
    __tablename__ = "insights"

    id                      = db.Column(db.Integer, primary_key=True)
    project_id              = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    content                 = db.Column(db.Text, nullable=False)  # the insight text / note

    # Optional foreign keys — an insight can be linked to a paper, an experiment, both, or neither
    related_paper_id        = db.Column(db.Integer, db.ForeignKey("papers.id"),      nullable=True)
    related_experiment_id   = db.Column(db.Integer, db.ForeignKey("experiments.id"), nullable=True)

    created_at              = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id":                    self.id,
            "project_id":            self.project_id,
            "content":               self.content,
            "related_paper_id":      self.related_paper_id,
            "related_experiment_id": self.related_experiment_id,
            "created_at":            self.created_at.isoformat(),
        }
