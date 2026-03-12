# routes/insight_routes.py
from flask import Blueprint, request, jsonify
from database import db
from models.insight_model import Insight

insight_bp = Blueprint("insights", __name__, url_prefix="/api/insights")


@insight_bp.route("", methods=["GET"])
def list_insights():
    project_id = request.args.get("project_id", type=int)
    stmt = db.select(Insight).order_by(Insight.created_at.desc())
    if project_id:
        stmt = stmt.where(Insight.project_id == project_id)
    insights = db.session.execute(stmt).scalars().all()
    return jsonify([i.to_dict() for i in insights]), 200


@insight_bp.route("", methods=["POST"])
def create_insight():
    data = request.get_json(silent=True) or {}

    project_id = data.get("project_id")
    content    = data.get("content", "").strip()

    if not project_id:
        return jsonify({"error": "project_id is required"}), 400
    if not content:
        return jsonify({"error": "content is required"}), 400

    insight = Insight(
        project_id=int(project_id),
        content=content,
        related_paper_id=data.get("related_paper_id"),
        related_experiment_id=data.get("related_experiment_id"),
    )
    db.session.add(insight)
    db.session.commit()
    return jsonify(insight.to_dict()), 201


@insight_bp.route("/<int:insight_id>", methods=["GET"])
def get_insight(insight_id):
    insight = db.get_or_404(Insight, insight_id)
    return jsonify(insight.to_dict()), 200


@insight_bp.route("/<int:insight_id>", methods=["PUT"])
def update_insight(insight_id):
    insight = db.get_or_404(Insight, insight_id)
    data    = request.get_json(silent=True) or {}

    for field in ["content", "related_paper_id", "related_experiment_id"]:
        if field in data:
            setattr(insight, field, data[field])

    db.session.commit()
    return jsonify(insight.to_dict()), 200


@insight_bp.route("/<int:insight_id>", methods=["DELETE"])
def delete_insight(insight_id):
    insight = db.get_or_404(Insight, insight_id)
    db.session.delete(insight)
    db.session.commit()
    return jsonify({"message": f"Insight {insight_id} deleted."}), 200
