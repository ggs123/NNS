# coding=utf-8
import model
import functools
import json
import os


class Searcher(object):
    def __init__(self, config):
        self.__config = config

    @staticmethod
    def build(config):
        with open(config['configPath'], 'r') as f:
            modelConfig = json.load(f)

        return Searcher(modelConfig)

    @functools.lru_cache()
    def __getSearcher(self, modelName):
        return model.create(self.__config[modelName])

    def search(self, query, k):
        return {modelName: self.__getSearcher(modelName).search(query, info['k'])[0] for modelName, info in k.items()}


if __name__ == '__main__':
    pass
