import importlib


def create(config):
    module = importlib.import_module(config['name'])
    searcher = module.Searcher.build(config['config'])

    return searcher


if __name__ == '__main__':
    # config = {
    #     'name': 'PQ',
    #     'config': {
    #         'encoder': {
    #             # "type": "train",
    #             # "config": {
    #             #     "datasetPath": "data/testData8x4.npy",
    #             #     "numOfSegments": 2,
    #             #     "numOfClasses": 4,
    #             #     "centroidsPath": "data/centroids8x4.npy"
    #             # }
    #             'type': 'load',
    #             "config": {
    #                 'centroidsPath': '../data/centroids8x4.npy'
    #             }
    #         },
    #         'data': {
    #             # "type": "train",
    #             # "dataPath": "data/testData8x4.npy",
    #             # "qdbPath": "data/qDataset8x4.npy"
    #             'type': 'load',
    #             'dataPath': '../data/qDataset8x4.npy'
    #         }
    #     }
    # }
    #
    # s = create(config)
    # print(s.search(np.random.rand(1, 4), 4))

    pass