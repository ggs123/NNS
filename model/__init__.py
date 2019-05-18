import importlib
import os
import sys

models = ['BruteForce', 'PQ']


def create(config):
    # ��model�ļ��м��뵽import������·����
    currentDir = os.path.dirname(__file__)
    if currentDir not in sys.path:
        sys.path.append(currentDir)

    module = importlib.import_module(config['name'])
    searcher = module.Searcher.build(config['config'])

    return searcher


if __name__ == '__main__':
    pass


