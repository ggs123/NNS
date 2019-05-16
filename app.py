# coding=utf-8
from flask import Flask, request, jsonify
import Search
import flask_cors

app = Flask(__name__)
flask_cors.CORS(app, supports_credentials=True)

config = {
    'model': {
        'name': 'model.PQ',
        'config': {
            'encoder': {
                "type": "train",
                "config": {
                    "datasetPath": "data/dataset.npy",
                    "numOfSegments": 2,
                    "numOfClasses": 16,
                    "centroidsPath": "data/centroids.npy"
                }
                # 'type': 'load',
                # "config": {
                #     'centroidsPath': 'data/centroids8x4.npy'
                # }
            },
            'data': {
                "type": "train",
                "dataPath": "data/dataset.npy",
                "qdbPath": "data/qDataset.npy"
                # 'type': 'load',
                # 'dataPath': 'data/qDataset.npy'
            }
        }
    },
    'db': {
        'dbPath': 'data/path.npy'
    },
    'extractorPath': './Extractor'
}

searcher = Search.Searcher(config)


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        # 获取数据
        data = request.form
        print(data)
        result, msg, paths = searcher.search(data['imageUrl'], int(data['pageNum']), int(data['pageSize']), int(data['k']))

        reply = {
            'result': result,
            'msg': msg,
            # 'data': ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg']
            'data': paths
        }
        print(reply)
        # return json.dumps(reply, ensure_ascii=False)
        return jsonify(reply)


if __name__ == '__main__':
    app.run()