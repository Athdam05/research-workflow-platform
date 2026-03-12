# routes/paper_routes.py
import os, sys

# Resolve backend/ directory correctly on Windows
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, BACKEND_DIR)

from flask import Blueprint, request, jsonify
from database import db
from models.paper_model import Paper
from utils.file_upload import save_file
from utils.ai_service import analyze_paper, analyze_paper_from_file

paper_bp = Blueprint("papers", __name__, url_prefix="/api/papers")


@paper_bp.route("", methods=["GET"])
def list_papers():
    project_id = request.args.get("project_id", type=int)
    stmt = db.select(Paper).order_by(Paper.created_at.desc())
    if project_id:
        stmt = stmt.where(Paper.project_id == project_id)
    return jsonify([p.to_dict() for p in db.session.execute(stmt).scalars().all()]), 200


@paper_bp.route("", methods=["POST"])
def create_paper():
    if request.content_type and "multipart/form-data" in request.content_type:
        data = request.form
    else:
        data = request.get_json(silent=True) or {}

    if not data.get("project_id"):
        return jsonify({"error": "project_id is required"}), 400
    if not data.get("title", "").strip():
        return jsonify({"error": "title is required"}), 400

    file_path = None
    if "file" in request.files:
        saved = save_file(request.files["file"])
        if saved is None:
            return jsonify({"error": "File type not allowed"}), 400
        file_path = saved

    title = data["title"].strip()

    # Use manually provided values if given, otherwise auto-generate with AI
    manual_summary  = data.get("summary",  "").strip()
    manual_keywords = data.get("keywords", "").strip()
    manual_concepts = data.get("concepts", "").strip()

    if not all([manual_summary, manual_keywords, manual_concepts]):
        print(f"🤖  Running AI analysis for: {title}")
        if file_path:
            ai_result = analyze_paper_from_file(title, file_path)
        else:
            ai_result = analyze_paper(title, data.get("link", "") or title)
    else:
        ai_result = {"summary": "", "keywords": "", "concepts": ""}

    paper = Paper(
        project_id=int(data["project_id"]),
        title=title,
        file_path=file_path,
        link=data.get("link", ""),
        tags=data.get("tags", ""),
        summary=manual_summary   or ai_result["summary"],
        keywords=manual_keywords or ai_result["keywords"],
        concepts=manual_concepts or ai_result["concepts"],
    )
    db.session.add(paper)
    db.session.commit()
    return jsonify(paper.to_dict()), 201


@paper_bp.route("/<int:paper_id>", methods=["GET"])
def get_paper(paper_id):
    return jsonify(db.get_or_404(Paper, paper_id).to_dict()), 200


@paper_bp.route("/<int:paper_id>", methods=["PUT"])
def update_paper(paper_id):
    paper = db.get_or_404(Paper, paper_id)
    data  = request.get_json(silent=True) or {}
    for field in ["title", "link", "tags", "summary", "keywords", "concepts"]:
        if field in data:
            setattr(paper, field, data[field])
    db.session.commit()
    return jsonify(paper.to_dict()), 200


@paper_bp.route("/<int:paper_id>/analyze", methods=["POST"])
def analyze_paper_endpoint(paper_id):
    """Re-run AI analysis on an existing paper."""
    paper = db.get_or_404(Paper, paper_id)
    print(f"🤖  Re-analyzing paper: {paper.title}")
    if paper.file_path:
        ai_result = analyze_paper_from_file(paper.title, paper.file_path)
    else:
        ai_result = analyze_paper(paper.title, paper.link or paper.title)
    paper.summary  = ai_result["summary"]
    paper.keywords = ai_result["keywords"]
    paper.concepts = ai_result["concepts"]
    db.session.commit()
    return jsonify({"message": "AI analysis complete", "paper": paper.to_dict()}), 200


@paper_bp.route("/<int:paper_id>", methods=["DELETE"])
def delete_paper(paper_id):
    paper = db.get_or_404(Paper, paper_id)
    db.session.delete(paper)
    db.session.commit()
    return jsonify({"message": f"Paper {paper_id} deleted."}), 200
