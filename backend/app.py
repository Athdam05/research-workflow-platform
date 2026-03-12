# app.py
import os
import sys

# Fix: abspath FIRST, then dirname — works correctly when __file__ is just "app.py"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from flask import Flask, jsonify
from flask_cors import CORS
from database import db, init_db
from models.project_model import Project
from models.paper_model import Paper
from models.experiment_model import Experiment
from models.insight_model import Insight
from models.relationship_model import Relationship
from routes.project_routes import project_bp
from routes.paper_routes import paper_bp
from routes.experiment_routes import experiment_bp
from routes.insight_routes import insight_bp
from routes.relationship_routes import relationship_bp


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]        = f"sqlite:///{os.path.join(BASE_DIR, 'research.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"]             = 16 * 1024 * 1024

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    init_db(app)

    app.register_blueprint(project_bp)
    app.register_blueprint(paper_bp)
    app.register_blueprint(experiment_bp)
    app.register_blueprint(insight_bp)
    app.register_blueprint(relationship_bp)

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "message": "RWIIP backend is running 🚀"}), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    return app


def print_routes(app):
    print("\n📡  Registered API routes:")
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        if rule.rule.startswith("/api"):
            methods = ", ".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
            print(f"   {methods:<20} {rule.rule}")
    print()


if __name__ == "__main__":
    app = create_app()
    print_routes(app)
    app.run(debug=True, host="0.0.0.0", port=5000)
