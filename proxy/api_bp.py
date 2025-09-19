from flask import Blueprint, jsonify, request
from auth_middleware import token_required


api_bp = Blueprint("api_bp", __name__, url_prefix="/api")


@api_bp.route("/movies/search")
@token_required
def get_search_results():
    try:
        pass
    except Exception as error:
        return jsonify({"error": error})
