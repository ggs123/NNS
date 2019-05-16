# coding=utf-8
import base64
import os
from pathlib import Path
import pickle
import numpy as np


def fun():
    return np.random.rand(1,5)


# class A(object):
#     def __init__(self, name):
#         self.__name = name
#
#     @property
#     def name(self):
#         return self.__name
#
#     @name.setter
#     def name(self, value):
#         self.__name = value


if __name__ == '__main__':
    pass

    # 利用base64解码，然后存到本地
    # picPath = "data/tmp/tmp.jpg"
    # with open(picPath, 'rb') as f:
    #     base64Data = base64.b64encode(f.read())
    #     print(base64Data)
    #
    #     s = base64.b64decode(base64Data)
    #     print(s)
    #     with open('data/tmp/s.jpg', 'wb') as f2:
    #         f2.write(s)


    # 执行exe文件来获取特征向量
    # 切换目录
    # path = "Extractor"
    # p = Path(path)
    # for x in p.iterdir():
    #     print(x)
    # # os.chdir(p)
    #
    # p2 = Path("tmp")
    # for x in p2.iterdir():
    #     print(x)

    # command = "E:\\workspace\\NNS\\Extractor\\deal_dir.exe ..\\data\\tmp"
    # x = os.system(command)
    #
    # print(x)


    # 执行位置的存储与读取
    # a = ['lskd', '2sdfs', 'slkdjf23', 'sdaoiwei']
    # path = 'data/path.pkl'
    #
    # with open(path, 'rb') as f:
    #     b = pickle.load(f)
    # print(b)
    # a = np.array([])
    # print(fun())
    # print(a)