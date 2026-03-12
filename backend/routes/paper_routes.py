# routes/paper_routes.py
from flask import Blueprint, request, jsonify
from database import db
from models.paper_model import Paper
from utils.file_upload import save_file

paper_bp = Blueprint("papers", __name__, url_prefix="/api/papers")


@paper_bp.route("", methods=["GET"])
def list_papers():
    project_id = request.args.get("project_id", type=int)
    stmt = db.select(Paper).order_by(Paper.created_at.desc())
    if project_id:
        stmt = stmt.where(Paper.project_id == project_id)
    papers = db.session.execute(stmt).scalars().all()
    return jsonify([p.to_dict() for p in papers]), 200


@paper_bp.route("", methods=["POST"])
def create_paper():
    if request.content_type and "multipart/form-data" in request.content_type:
        data = request.form
    else:
        data = request.get_json(silent=True) or {}

    project_id = data.get("project_id")
    title      = data.get("title", "").strip()

    if not project_id:
        return jsonify({"error": "project_id is required"}), 400
    if not title:
        return jsonify({"error": "title is required"}), 400

    file_path = None
    if "file" in request.files:
        saved = save_file(request.files["file"])
        if saved is None:
            return jsonify({"error": "File type not allowed"}), 400
        file_path = saved

    paper = Paper(
        project_id=int(project_id),
        title=title,
        file_path=file_path,
        link=data.get("link", ""),
        tags=data.get("tags", ""),
        summary=data.get("summary", ""),
        keywords=data.get("keywords", ""),
        concepts=data.get("concepts", ""),
    )
    db.session.add(paper)
    db.session.commit()
    return jsonify(paper.to_dict()), 201


@paper_bp.route("/<int:paper_id>", methods=["GET"])
def get_paper(paper_id):
    paper = db.get_or_404(Paper, paper_id)
    return jsonify(paper.to_dict()), 200


@paper_bp.route("/<int:paper_id>", methods=["PUT"])
def update_paper(paper_id):
    paper = db.get_or_404(Paper, paper_id)
    data  = request.get_json(silent=True) or {}

    for field in ["title", "link", "tags", "summary", "keywords", "concepts"]:
        if field in data:
            setattr(paper, field, data[field])

    db.session.commit()
    return jsonify(paper.to_dict()), 200


@paper_bp.route("/<int:paper_id>", methods=["DELETE"])
def delete_paper(paper_id):
    paper = db.get_or_404(Paper, paper_id)
    db.session.delete(paper)
    db.session.commit()
    return jsonify({"message": f"Paper {paper_id} deleted."}), 200
