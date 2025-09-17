import os
import jwt
import bcrypt
import psycopg2
import psycopg2.extras
from flask import Blueprint, jsonify, request, g
from db_helpers import get_db_connection
from auth_middleware import token_required

lists_bp = Blueprint("lists_bp", __name__)

"""
/lists # all lists
/topics/topic_id # all lists in a topic

UPDATE
/topics/topic_id/lists/list_id # list show page

DELETE
/topics/topic_id/lists/list_id # list show page

"""


# CREATE A LIST
@lists_bp.route("/topics/<topic_id>/lists", methods=["POST"])
@token_required
def create_list(topic_id):
    try:

        list_data = request.get_json()
        list_data["author"] = g.user["id"]
        list_data["topic"] = int(topic_id)
        if len(list_data["list_items"]) != 5:
            return jsonify({"error": "List must have 5 elements"}), 400

        conn = get_db_connection()
        curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # INSERT INTO THE LISTS TABLE
        curs.execute(
            """
            INSERT INTO lists (topic_id, author_id)
            VALUES (%s, %s)
            RETURNING *
            """,
            (list_data["topic"], list_data["author"]),
        )
        created_list = curs.fetchone()

        # ADD EACH LIST ITEMS TO THE LIST_ITEMS TABLE
        created_list_items = []
        for idx, item in enumerate(list_data["list_items"]):
            item["rank"] = idx + 1
            curs.execute(
                """
                INSERT INTO list_items (list_id, rank, external_id, notes)
                VALUES (%s,%s,%s,%s)
                RETURNING *
                """,
                (created_list["id"], item["rank"], item["external_id"], item["notes"]),
            )
            created_item = curs.fetchone()
            created_list_items.append(created_item)

        created_list["list_items"] = created_list_items
        conn.commit()
        conn.close()
        return jsonify(created_list), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500
