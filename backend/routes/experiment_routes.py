# routes/experiment_routes.py
from flask import Blueprint, request, jsonify
from database import db
from models.experiment_model import Experiment

experiment_bp = Blueprint("experiments", __name__, url_prefix="/api/experiments")


@experiment_bp.route("", methods=["GET"])
def list_experiments():
    project_id = request.args.get("project_id", type=int)
    stmt = db.select(Experiment).order_by(Experiment.created_at.desc())
    if project_id:
        stmt = stmt.where(Experiment.project_id == project_id)
    experiments = db.session.execute(stmt).scalars().all()
    return jsonify([e.to_dict() for e in experiments]), 200


@experiment_bp.route("", methods=["POST"])
def create_experiment():
    data = request.get_json(silent=True) or {}

    project_id = data.get("project_id")
    title      = data.get("title", "").strip()

    if not project_id:
        return jsonify({"error": "project_id is required"}), 400
    if not title:
        return jsonify({"error": "title is required"}), 400

    experiment = Experiment(
        project_id=int(project_id),
        title=title,
        hypothesis=data.get("hypothesis", ""),
        method=data.get("method", ""),
        result=data.get("result", ""),
        related_paper_id=data.get("related_paper_id"),
    )
    db.session.add(experiment)
    db.session.commit()
    return jsonify(experiment.to_dict()), 201


@experiment_bp.route("/<int:experiment_id>", methods=["GET"])
def get_experiment(experiment_id):
    experiment = db.get_or_404(Experiment, experiment_id)
    return jsonify(experiment.to_dict()), 200


@experiment_bp.route("/<int:experiment_id>", methods=["PUT"])
def update_experiment(experiment_id):
    experiment = db.get_or_404(Experiment, experiment_id)
    data       = request.get_json(silent=True) or {}

    for field in ["title", "hypothesis", "method", "result", "related_paper_id"]:
        if field in data:
            setattr(experiment, field, data[field])

    db.session.commit()
    return jsonify(experiment.to_dict()), 200


@experiment_bp.route("/<int:experiment_id>", methods=["DELETE"])
def delete_experiment(experiment_id):
    experiment = db.get_or_404(Experiment, experiment_id)
    db.session.delete(experiment)
    db.session.commit()
    return jsonify({"message": f"Experiment {experiment_id} deleted."}), 200
