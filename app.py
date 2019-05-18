# coding=utf-8
from flask import Flask, request, jsonify
import Search
import flask_cors
import json

app = Flask(__name__)
flask_cors.CORS(app, supports_credentials=True)

config = {
    'model': {
        'name': 'MixSearch',
        'config': {
            'configPath': "model/modelConfig.json"
        }
    },
    'db': {
        'dbPath': 'data/path.npy'
    },
    'featureExtractor': {
        'extractorPath': './Extractor'
    }
}

searcher = Search.Searcher(config)


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        # 获取数据
        data = request.form
        print(data)

        result, msg, paths = searcher.search(data['image'], json.loads(data['pageInfo']))
        # result, msg, paths = 0, "ok", ["1.jpg"]

        reply = {
            'result': result,
            'msg': msg,
            'data': paths
        }
        return jsonify(reply)


@app.route('/fetchModelName', methods=['GET'])
def fetchModelName():
    if request.method == 'GET':
        result, msg, data = searcher.getModelName()

        reply = {
            'result': result,
            'msg': msg,
            'data': data
        }
        return jsonify(reply)


if __name__ == '__main__':
    app.run()
