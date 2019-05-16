# coding=utf-8
import numpy as np


class Searcher(object):
    def __init__(self, dataset):
        self.__dataset = dataset

    @staticmethod
    def build(config):
        dataConfig = config['data']
        dataset = np.load(dataConfig['path'])

        return Searcher(dataset)

    def search(self, query, k):
        def _find(point: np.ndarray) -> np.ndarray:
            distances = np.linalg.norm(point - self.__dataset, axis=1)
            candidates = np.argpartition(distances, k)[:k]
            return candidates[np.argsort(distances[candidates])]
        return np.apply_along_axis(_find, 1, query if query.ndim == 2 else query[None])


if __name__ == '__main__':
    # ##################################
    # # 使用范例
    # ##################################

    config = {
        'data': {
            "path": "../data/dataset.npy"
        }
    }
    s1 = Searcher.build(config)

    print(s1.search(np.random.rand(1, 62).astype(np.float), 6))
