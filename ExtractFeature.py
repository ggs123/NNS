# coding=utf-8
import numpy as np
import pathlib
import os
import pandas as pd


class FeatureExtractor(object):
    def __init__(self, config):
        self.__extractorPath = config['extractorPath']
        extractorPath = pathlib.Path(self.__extractorPath)
        if not (extractorPath.exists() and extractorPath.is_dir()):
            raise ValueError('特征提取器路径不正确')

    def getFeature(self, srcPath):
        # pandas实现数据读取
        features = pd.read_csv(srcPath, sep=' ', header=None, encoding='gbk')
        return list(features.values[:, 0]), list(features.values[:, 1:].astype(np.float32))

    def __extract(self, root):
        root = pathlib.Path(root)
        if not root.is_dir():
            return 1, '希望是个目录而不是文件', None, None
        absolutePath = root.absolute()

        # 切换到特征提取可执行程序的目录下
        cwd = os.getcwd()
        # 硬编码, 已改为配置文件指定
        # extractorPath = pathlib.Path('Extractor')
        extractorPath = pathlib.Path(self.__extractorPath)
        os.chdir(extractorPath)

        # 提取特征
        cmd = f'deal_dir.exe {absolutePath}'
        # cmd = f'deal_dir.exe test'
        x = os.system(cmd)
        os.chdir(cwd)
        if x != 0:
            return 1, '提取特征出错', None, None

        # 获取提取的特征
        try:
            resultPath = absolutePath / 'match_feature.dat'
            paths, features = self.getFeature(resultPath)
        except Exception as err:
            paths = []
            features = []

        allImage = set(absolutePath.iterdir())
        extractedImage = set([pathlib.Path(path) for path in paths])
        exceptionImage = allImage - extractedImage - set([resultPath])

        if exceptionImage:
            return 0, f'如下图片提取失败:{exceptionImage}', paths, features
        if not extractedImage:
            return 1, "该目录下没有图片", None, None

        # 将相对路径中的'\\'替换为'/'
        paths = [path.replace('\\', '/') for path in paths]

        return 0, 'OK', paths, features

    def extract(self, root, depth):
        if not (depth == 0 or depth == 1):
            return 1, "depth只能为0或者1", None, None

        root = pathlib.Path(root)
        if not (root.exists() and root.is_dir()):
            return 1, '图片路径不正确，希望是个文件夹', None, None

        if depth == 0:
            result, msg, _paths, _features = self.__extract(root)
            return result, msg, np.array(_paths), np.array(_features)
        else:
            msg = ''
            features = []
            paths = []

            for subDir in root.iterdir():
                result, _msg, _paths, _features = self.__extract(subDir)
                msg = f'{msg}{subDir}:{_msg}\n'
                if result == 0:
                    features = features + _features
                    paths = paths + _paths

            # 将所有图片的路径变为相对根目录的路径
            rootStr = f'{str(root.absolute())}/'.replace('\\', '/')
            paths = [path.replace(rootStr, '') for path in paths]

            return 0, msg, np.array(paths), np.array(features)


if __name__ == '__main__':
    # ##################################
    # # 使用范例
    # ##################################
    path = 'data/image'
    config = {
        'extractorPath': './Extractor'
    }

    featureExtractor = FeatureExtractor(config)
    print(featureExtractor.extract(path, 1))
