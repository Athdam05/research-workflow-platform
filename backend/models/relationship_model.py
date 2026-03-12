import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/..")))

from database import db

VALID_TYPES = ["paper", "experiment", "insight", "concept"]


class Relationship(db.Model):
    __tablename__ = "relationships"

    id          = db.Column(db.Integer, primary_key=True)
    source_type = db.Column(db.String(50),  nullable=False)
    source_id   = db.Column(db.Integer,     nullable=False)
    target_type = db.Column(db.String(50),  nullable=False)
    target_id   = db.Column(db.Integer,     nullable=False)
    label       = db.Column(db.String(100), default="related_to")

    def to_dict(self):
        return {
            "id":          self.id,
            "source_type": self.source_type,
            "source_id":   self.source_id,
            "target_type": self.target_type,
            "target_id":   self.target_id,
            "label":       self.label,
        }
