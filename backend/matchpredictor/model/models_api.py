from dataclasses import dataclass

from flask import Blueprint, jsonify, Response

from matchpredictor.model.model_provider import ModelProvider


@dataclass(frozen=True)
class ModelInfo(object):
    name: str
    predicts_in_progress: bool


def models_api(model_provider: ModelProvider) -> Blueprint:
    api = Blueprint("models_api", __name__)

    @api.route("/models", methods=["GET"])
    def models() -> Response:
        return jsonify({
            "models": [ModelInfo(model.name, model.predicts_in_progress()) for model in model_provider.list()]
        })

    return api
