import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/..")))

from flask import Blueprint, request, jsonify
from database import db
from models.relationship_model import Relationship, VALID_TYPES
from models.paper_model import Paper
from models.experiment_model import Experiment
from models.insight_model import Insight

relationship_bp = Blueprint("relationships", __name__, url_prefix="/api/relationships")


@relationship_bp.route("", methods=["GET"])
def list_relationships():
    source_type = request.args.get("source_type")
    source_id   = request.args.get("source_id",   type=int)
    target_type = request.args.get("target_type")
    target_id   = request.args.get("target_id",   type=int)
    stmt = db.select(Relationship)
    if source_type: stmt = stmt.where(Relationship.source_type == source_type)
    if source_id:   stmt = stmt.where(Relationship.source_id   == source_id)
    if target_type: stmt = stmt.where(Relationship.target_type == target_type)
    if target_id:   stmt = stmt.where(Relationship.target_id   == target_id)
    return jsonify([r.to_dict() for r in db.session.execute(stmt).scalars().all()]), 200


@relationship_bp.route("", methods=["POST"])
def create_relationship():
    data = request.get_json(silent=True) or {}
    for field in ["source_type", "source_id", "target_type", "target_id"]:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400
    if data["source_type"] not in VALID_TYPES:
        return jsonify({"error": f"source_type must be one of: {', '.join(VALID_TYPES)}"}), 400
    if data["target_type"] not in VALID_TYPES:
        return jsonify({"error": f"target_type must be one of: {', '.join(VALID_TYPES)}"}), 400
    rel = Relationship(
        source_type=data["source_type"],
        source_id=int(data["source_id"]),
        target_type=data["target_type"],
        target_id=int(data["target_id"]),
        label=data.get("label", "related_to"),
    )
    db.session.add(rel)
    db.session.commit()
    return jsonify(rel.to_dict()), 201


@relationship_bp.route("/<int:rel_id>", methods=["GET"])
def get_relationship(rel_id):
    return jsonify(db.get_or_404(Relationship, rel_id).to_dict()), 200


@relationship_bp.route("/<int:rel_id>", methods=["DELETE"])
def delete_relationship(rel_id):
    rel = db.get_or_404(Relationship, rel_id)
    db.session.delete(rel)
    db.session.commit()
    return jsonify({"message": f"Relationship {rel_id} deleted."}), 200


@relationship_bp.route("/graph", methods=["GET"])
def project_graph():
    project_id = request.args.get("project_id", type=int)
    if not project_id:
        return jsonify({"error": "project_id query param is required"}), 400

    papers      = db.session.execute(db.select(Paper).where(Paper.project_id == project_id)).scalars().all()
    experiments = db.session.execute(db.select(Experiment).where(Experiment.project_id == project_id)).scalars().all()
    insights    = db.session.execute(db.select(Insight).where(Insight.project_id == project_id)).scalars().all()

    paper_ids      = {p.id for p in papers}
    experiment_ids = {e.id for e in experiments}
    insight_ids    = {i.id for i in insights}

    def in_project(rel):
        def belongs(typ, eid):
            if typ == "paper":      return eid in paper_ids
            if typ == "experiment": return eid in experiment_ids
            if typ == "insight":    return eid in insight_ids
            return True
        return belongs(rel.source_type, rel.source_id) or belongs(rel.target_type, rel.target_id)

    all_rels = db.session.execute(db.select(Relationship)).scalars().all()
    edges    = [r.to_dict() for r in all_rels if in_project(r)]
    nodes    = (
        [{"id": f"paper_{p.id}",      "type": "paper",      "label": p.title}        for p in papers]
      + [{"id": f"experiment_{e.id}", "type": "experiment", "label": e.title}        for e in experiments]
      + [{"id": f"insight_{i.id}",    "type": "insight",    "label": i.content[:60]} for i in insights]
    )
    return jsonify({"nodes": nodes, "edges": edges}), 200
