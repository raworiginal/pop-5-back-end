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
        return jsonify(created_list), 201
    except Exception as error:
        return jsonify({"error": str(error)}), 500


# READ ALL LISTS
@lists_bp.route("/lists", methods=["GET"])
@token_required
def lists_index():
    try:
        conn = get_db_connection()
        curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        curs.execute(
            """
            SELECT * FROM lists_index
            """
        )
        lists = curs.fetchall()
        conn.commit()
        conn.close()
        return jsonify(lists), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


# SHOW LIST ROUTE BY LIST ID
@lists_bp.route("/lists/<list_id>", methods=["GET"])
@token_required
def show_list(list_id):
    try:
        conn = get_db_connection()
        curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        curs.execute(
            """
            SELECT * FROM lists_index WHERE id = %s
            """,
            (list_id,),
        )
        list = curs.fetchone()
        if list is None:
            return jsonify({"error": "List not found"}), 404
        conn.commit()
        conn.close()
        return jsonify(list)
    except Exception as error:
        return jsonify({"error": str(error)}), 500


# UPDATE LIST ROUTE BY LIST ID
@lists_bp.route("/lists/<list_id>", methods=["PUT"])
@token_required
def update_list(list_id):
    try:
        updated_list_data = request.get_json()
        if len(updated_list_data["list_items"]) != 5:
            return jsonify({"error": "List must have 5 items"}), 400
        conn = get_db_connection()
        curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        curs.execute(
            """
            SELECT * FROM list_items WHERE list_id = %s
            """,
            (list_id,),
        )
        list_items_to_update = curs.fetchall()
        if not list_items_to_update:
            return jsonify({"error": "list not found"}), 404

        curs.execute(
            """
            SELECT author_id as id FROM lists WHERE id = %s 
            """,
            (list_id,),
        )
        author = curs.fetchone()
        if author["id"] is not g.user["id"]:
            return jsonify({"error": "Unauthorized"}), 401
        for idx, item in enumerate(list_items_to_update):
            print(f"Index = {idx}: item id = {item['id']} ")
            updated_list_item = updated_list_data["list_items"][idx]
            updated_rank = idx + 1
            print(updated_list_item)
            curs.execute(
                """
                UPDATE list_items SET rank = %s, external_id = %s, notes =%s
                WHERE id = %s
                RETURNING *
                """,
                (
                    updated_rank,
                    updated_list_item["external_id"],
                    updated_list_item["notes"],
                    item["id"],
                ),
            )
        curs.execute("SELECT * FROM list_items WHERE list_id = %s", (list_id,))
        updated_list_items = curs.fetchall()

        conn.commit()
        conn.close()
        return jsonify(updated_list_items), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500
