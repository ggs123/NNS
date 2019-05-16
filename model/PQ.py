# coding=utf-8
import numpy as np
import scipy.cluster.vq as scvq


class Encoder(object):
    def __init__(self, centroids):
        self.__centroids = centroids
        self.__numOfSegments, self.__numOfClasses, _ = self.__centroids.shape

    @staticmethod
    def load(config):
        centroids = np.load(config['centroidsPath'])
        return Encoder(centroids)

    @staticmethod
    def train(config):
        data = np.load(config['datasetPath'])
        numOfSegments = int(config['numOfSegments'])
        numOfClasses = int(config['numOfClasses'])

        cl = [scvq.kmeans2(subPoints, numOfClasses, minit='points') for subPoints in np.hsplit(data, numOfSegments)]
        centroids = np.vstack(map(lambda tp: tp[0][None], cl))

        # 保存质心
        if config['centroidsPath']:
            np.save(config['centroidsPath'], centroids)

        return Encoder(centroids)

    @staticmethod
    def build(config):
        try:
            print(config)
            return {'load': Encoder.load, 'train': Encoder.train}[config['type']](config['config'])
        except KeyError as e:
            raise ValueError(f"Unkonwn type:{config['type']},expected 'load' or 'train'")

    def getDistance(self, x, y):
        dist = 0
        for a, b in zip(x, y):
            dist += (a - b) * (a - b)
        return dist

    def _quantize(self, vector, codebook):
        dists = [(i, self.getDistance(vector, codebook[i])) for i in range(codebook.shape[0])]
        dists = sorted(dists, key=lambda x: x[1])
        return dists[0][0]

    def quantize(self, vectors, codebook, pqCode):
        for i in range(vectors.shape[0]):
            pqCode[i] = self._quantize(vectors[i], codebook)

    def encode(self, vectors):
        m, k, Ds = self.__centroids.shape
        if m * Ds != vectors.shape[1]:
            raise ValueError("向量维数与码书不一致")

        pqCode = np.empty((m, vectors.shape[0]), np.int32)

        for i in range(m):
            subVectors = vectors[:, i * Ds: (i + 1) * Ds]
            self.quantize(subVectors, self.__centroids[i], pqCode[i])

        return pqCode.T

    @property
    def centroids(self):
        return self.__centroids


class Searcher(object):
    def __init__(self, encoder, dataset):
        self.__encoder = encoder
        self.__qDataset = dataset

    @staticmethod
    def build(config):
        encoder = Encoder.build(config['encoder'])
        dataConfig = config['data']
        qDataset = {"load": lambda x: x, "train": encoder.encode}[dataConfig['type']](np.load(dataConfig['dataPath']))

        if dataConfig['type'] == 'train' and dataConfig['qdbPath']:
            np.save(dataConfig['qdbPath'], qDataset)

        return Searcher(encoder, qDataset)

    def search(self, query, k):
        def _find(point: np.ndarray) -> np.ndarray:
            lut = np.square(np.linalg.norm(np.array(np.hsplit(point, self.__encoder.centroids.shape[0]))[:, None, :] - self.__encoder.centroids, axis=2))
            distances = np.array([np.sum(lut[np.arange(self.__encoder.centroids.shape[0]), qPoint]) for qPoint in self.__qDataset])
            candidates = np.argpartition(distances, k)[:k]
            return candidates[np.argsort(distances[candidates])]
        return np.apply_along_axis(_find, 1, query if query.ndim == 2 else query[None])


if __name__ == '__main__':
    config = {
        'encoder': {
            "type": "train",
            "config": {
                "datasetPath": "../data/dataset.npy",
                "numOfSegments": 31,
                "numOfClasses": 16,
                "centroidsPath": "../data/centroids.npy"
            }
            # 'type': 'load',
            # "config": {
            #     'centroidsPath': '../data/centroids8x4.npy'
            # }
        },
        'data': {
            "type": "train",
            "dataPath": "../data/dataset.npy",
            "qdbPath": "../data/qDataset.npy"
            # 'type': 'load',
            # 'dataPath': 'data/qDataset.npy'
        }
    }
    s1 = Searcher.build(config)

    print(s1.search(np.random.rand(1, 62).astype(np.float), 6))
