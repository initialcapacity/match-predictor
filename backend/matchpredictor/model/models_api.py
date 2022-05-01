from flask import Blueprint, jsonify, Response

from matchpredictor.model.model_provider import ModelProvider


def models_api(model_provider: ModelProvider) -> Blueprint:
    api = Blueprint("models_api", __name__)

    @api.route("/models", methods=["GET"])
    def models() -> Response:
        return jsonify({
            "models": [model.name for model in model_provider.list()]
        })

    return api
