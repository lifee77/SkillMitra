from flask import Blueprint, jsonify

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return jsonify({
        "message": "Welcome to SkillMitra API!",
        "status": "success",
        "routes": {
            "data": "/data",
            "media": "/media",
            "recommendation": "/recommendation"
        }
    })
