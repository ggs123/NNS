# coding=utf-8
from flask import Flask, request, jsonify
import Search
import flask_cors

app = Flask(__name__)
flask_cors.CORS(app, supports_credentials=True)

pqConfig = {'name': 'model.PQ',
            'config': {
                'encoder': {
                    "type": "train",
                    "config": {
                        "datasetPath": "data/dataset.npy",
                        "numOfSegments": 31,
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
}

bruteForceConfig = {'name': 'model.BruteForce',
                    'config': {
                        'data': {
                            "path": "data/dataset.npy"
                        }
                    }
}

config = {
    'model': {
        'name': 'model.MixSearch',
        'config': {
            'models': [pqConfig]
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

        result, msg, paths = searcher.search(data['imageUrl'], int(data['pageNum']), int(data['pageSize']), int(data['k']))
        paths = [path.replace('\\', '/') for path in paths]
        print(paths)
        reply = {
            'result': result,
            'msg': msg,
            'data': paths
        }
        return jsonify(reply)


if __name__ == '__main__':
    app.run()
