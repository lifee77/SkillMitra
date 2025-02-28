from flask import Blueprint, request, jsonify
from modules.recommendation import get_recommendations

recommendation_bp = Blueprint('recommendation_bp', __name__)

@recommendation_bp.route('/', methods=['GET'])
def recommendations():
    """
    Endpoint to get course recommendations based on a user_id query parameter.
    """
    user_id = request.args.get('user_id', '')
    recs = get_recommendations(user_id)
    return jsonify({'user_id': user_id, 'recommendations': recs})
