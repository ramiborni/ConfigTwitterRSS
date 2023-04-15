import toml
from flask import Flask, request
from flask_cors import CORS
import tomllib
import json

app = Flask(__name__)
CORS(app)

user = {
    'username': 'admin',
    'password': 'password'
}

CONFIG_PATH = "/home/rami/PycharmProjects/TwitterRSSV2/config.toml"


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        request_body = request.get_json()
        username = request_body['username']
        password = request_body['password']
        if username == user['username'] and password == user['password']:
            return app.response_class(
                status=200,
                mimetype='application/json'
            )
        else:
            return app.response_class(
                status=401,
                mimetype='application/json'
            )
    else:
        return app.response_class(
            status=404,
            mimetype='application/json'
        )


@app.route("/get-config", methods=['GET'])
def get_config():
    if request.method == 'GET':
        with open(CONFIG_PATH, mode="rb") as config_file:
            config = tomllib.load(config_file)
            return app.response_class(
                status=200,
                mimetype='application/json',
                response=json.dumps(config['scrapper_config'])
            )


@app.route("/update-config", methods=['POST'])
def update_config():
    if request.method == 'POST':
        with open(CONFIG_PATH, "w") as toml_file:
            print( json.loads(request.data))
            toml.dump({
                "scrapper_config":  json.loads(request.data)
            }, toml_file)
        return app.response_class(
            status=200,
            mimetype='application/json',
        )
    else:
        return 404


if __name__ == '__main__':
    app.run()
