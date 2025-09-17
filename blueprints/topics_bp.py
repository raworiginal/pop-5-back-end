import os
import jwt
import bcrypt
import psycopg2
import psycopg2.extras
from flask import Blueprint, jsonify, request, g
from db_helpers import get_db_connection
from auth_middleware import token_required

topics_bp = Blueprint("topics_bp", __name__, url_prefix="/topics")


# CREATE A TOPIC
@topics_bp.route("/", methods=["POST"])
@token_required
def create_topic():
    try:
        new_topic = request.get_json()
        new_topic["owner"] = g.user["id"]
        conn = get_db_connection()
        curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        curs.execute(
            """
            INSERT INTO topics (owner, title, description,category)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """,
            (
                new_topic["owner"],
                new_topic["title"],
                new_topic["description"],
                new_topic["category"],
            ),
        )
        created_topic = curs.fetchone()
        conn.commit()
        conn.close()
        return jsonify(created_topic), 201
    except Exception as error:
        return jsonify({"error": str(error)}), 500


# READ ALL TOPICS
@topics_bp.route("/", methods=["GET"])
@token_required
def topics_index():
    try:
        conn = get_db_connection()
        curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        curs.execute(
            """
            SELECT 
            t.id, t.title, t.description, t.category, t.owner, t.created_at,
            json_build_object(
                'id', t.owner,
                'username', u.username
            ) AS owner
            FROM topics t
            JOIN users u
            ON t.owner = u.id
            """
        )
        topics = curs.fetchall()
        conn.commit()
        conn.close()
        return jsonify(topics), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500
