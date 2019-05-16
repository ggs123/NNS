# coding=utf-8
import numpy as np


class Db(object):
    def __init__(self, paths):
        self.__paths = paths

    @staticmethod
    def load(config):
        dbPath = config['dbPath']

        paths = np.load(dbPath)

        return Db(paths)

    def getPath(self, indexs):
        # paths = [self.__paths[index] for index in indexs]
        paths = list(self.__paths[indexs])
        return paths


if __name__ == '__main__':
    # ##################################
    # # 使用范例
    # ##################################
    config = {
        'dbPath': 'data/path.npy'
    }
    db = Db.load(config)

    print(db.getPath([1, 2]))
