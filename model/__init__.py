import importlib
import os
import sys

models = []


def create(config):
    # ��model�ļ��м��뵽import������·����
    currentDir = os.path.dirname(__file__)
    if currentDir not in sys.path:
        sys.path.append(currentDir)

    module = importlib.import_module(config['name'])
    searcher = module.Searcher.build(config['config'])

    return searcher


def registeModel(modelNames):
    global models
    models.extend(modelNames)


if __name__ == '__main__':
    pass


