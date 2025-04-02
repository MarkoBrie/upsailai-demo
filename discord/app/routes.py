from flask import Blueprint, jsonify


print(f"?. import file /discord/app/routes.py)")

# Create a Blueprint instance
main_bp = Blueprint("main", __name__)


# Define a route for this Blueprint
@main_bp.route("/ready", methods=["GET"])
def ready():
    return jsonify({"status": "ready"}), 200
