from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
from type_defs import schema

app = Flask(__name__)


@app.route("/")
def index():
    return "Navigate to /graphql"


@app.route("/graphql", methods=["GET"])
def playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=None, debug=app.debug)
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
