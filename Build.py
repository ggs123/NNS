# coding=utf-8
import numpy as np
import ExtractFeature


def build(picPath, featurePath, pathPath, extractorPath):
    result, msg, paths, features = ExtractFeature.extract(extractorPath, picPath, 1)

    if result:
        print(f'提取特征失败:{msg}')
    else:
        print(msg)
    if paths.shape[0] != features.shape[0]:
        print("特征数目与路径数目不一致，构建过程出错")

    # 分开保存
    np.save(featurePath, features)
    np.save(pathPath, paths)
    # 保存到一个文件夹下
    # with open(featurePath, 'wb') as f:
    #     np.save(f, features)
    #     np.save(f, paths)


if __name__ == '__main__':
    picPath = 'data/image'
    featurePath = 'data/dataset.npy'
    pathPath = 'data/path.npy'
    extractorPath = './Extractor'

    # build(picPath, featurePath, pathPath, extractorPath)

    feature = np.load(featurePath)
    print(feature)
    print(feature.shape)

    path = np.load(pathPath)
    print(path)
    print(path.shape)

    # feature1 = feature[:, :17]
    # feature2 = feature[:, 17:]
    #
    # print(feature1.shape)
    # print(feature2.shape)
    #
    # # print(np.all(feature1 == 0))
    # np.save("data/datasetWithout0.npy", feature2)
