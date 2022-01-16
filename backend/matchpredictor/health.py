from flask import Blueprint, jsonify, Response


def health_api() -> Blueprint:
    api = Blueprint("health_api", __name__)

    @api.route("/", methods=["GET"])
    def health() -> Response:
        return jsonify({"status": "UP"})

    return api
