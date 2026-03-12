# routes/project_routes.py
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Blueprint, request, jsonify
from database import db
from models.project_model import Project

project_bp = Blueprint("projects", __name__, url_prefix="/api/projects")


@project_bp.route("", methods=["GET"])
def list_projects():
    projects = db.session.execute(db.select(Project).order_by(Project.created_at.desc())).scalars().all()
    return jsonify([p.to_dict() for p in projects]), 200


@project_bp.route("", methods=["POST"])
def create_project():
    data = request.get_json(silent=True) or {}
    if not data.get("title"):
        return jsonify({"error": "title is required"}), 400

    project = Project(
        title=data["title"].strip(),
        description=data.get("description", "").strip(),
    )
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201


@project_bp.route("/<int:project_id>", methods=["GET"])
def get_project(project_id):
    project = db.get_or_404(Project, project_id)
    result = project.to_dict()
    result["papers"]      = [p.to_dict() for p in project.papers]
    result["experiments"] = [e.to_dict() for e in project.experiments]
    result["insights"]    = [i.to_dict() for i in project.insights]
    return jsonify(result), 200


@project_bp.route("/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    project = db.get_or_404(Project, project_id)
    data    = request.get_json(silent=True) or {}

    if "title" in data:
        project.title = data["title"].strip()
    if "description" in data:
        project.description = data["description"].strip()

    db.session.commit()
    return jsonify(project.to_dict()), 200


@project_bp.route("/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    project = db.get_or_404(Project, project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": f"Project {project_id} deleted."}), 200
