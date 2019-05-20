# coding=utf-8
import base64
import Db
import model
import ExtractFeature
import functools


RESULT_OK = 0
RESULT_ERROR = 1
MSG_OK = 'OK'


class Searcher(object):
    def __init__(self, config):
        self.__db = Db.Db.load(config['db'])
        self.__searcher = model.create(config['model'])
        self.__featureExtractor = ExtractFeature.FeatureExtractor(config['featureExtractor'])

    def __saveImage(self, data, path, fileName):
        picData = data.split(",")[1]
        decodedPicData = base64.b64decode(picData)
        path = f'{path}/{fileName}'

        with open(path, 'wb') as f:
            f.write(decodedPicData)

    @functools.lru_cache()
    def __extract(self, data):
        path = 'data/tmp'  # 图片存放路径
        fileName = 'tmp.jpg'
        print('111')
        # 将图片保存到data/tmp下，图片名为tmp.jpg
        try:
            self.__saveImage(data, path, fileName)
        except Exception as err:
            return RESULT_ERROR, "图片数据不正确", None

        # 提取图片的特征
        return self.__featureExtractor.extract(path, 0)

    def search(self, data, pageInfo):
        # 提取特征
        result, msg, _, features = self.__extract(data)

        if result != 0 or features.shape[0] != 1:
            return RESULT_ERROR, msg, None

        # 搜索
        result = self.__searcher.search(features[0], pageInfo)
        print(result)

        for modelName, info in pageInfo.items():
            pageNum = info['pageNum']
            pageSize = info['pageSize']

            indexes = result[modelName][pageNum * pageSize:(pageNum + 1) * pageSize]
            try:
                indexes = self.__db.getPath(indexes)
            except Exception as err:
                return RESULT_ERROR, "查询出错", None
            result[modelName] = indexes

        return RESULT_OK, MSG_OK, result

    def getModelName(self):
        return RESULT_OK, MSG_OK, model.models
