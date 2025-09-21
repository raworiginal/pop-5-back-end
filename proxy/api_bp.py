from flask import Blueprint, jsonify, request
from auth_middleware import token_required
from .movies_tmdb import search_for_movie

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")


@api_bp.route("/movies/search", methods=["POST"])
@token_required
def get_search_results():
    try:
        search_query_data = request.get_json()
        results = search_for_movie(search_query_data)
        return jsonify(results), 200
    except Exception as error:
        return jsonify({"error": error}), 500
