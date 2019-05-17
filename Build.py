# coding=utf-8
import numpy as np
import ExtractFeature


def build(root, featurePath, pathPath, config):
    featureExtractor = ExtractFeature.FeatureExtractor(config)

    result, msg, paths, features = featureExtractor.extract(root, 1)

    if result:
        print(f'提取特征失败:{msg}')
        return

    if paths.shape[0] != features.shape[0]:
        print("特征数目与路径数目不一致，构建过程出错")
        return

    print(msg)

    # 分开保存
    np.save(featurePath, features)
    np.save(pathPath, paths)
    # 保存到一个文件夹下
    # with open(featurePath, 'wb') as f:
    #     np.save(f, features)
    #     np.save(f, paths)


if __name__ == '__main__':
    # ##################################
    # # 使用范例
    # ##################################
    root = 'data/image'
    featurePath = 'data/dataset.npy'
    pathPath = 'data/path.npy'
    config = {
        'extractorPath': './Extractor'
    }

    build(root, featurePath, pathPath, config)

    feature = np.load(featurePath)
    print(feature)
    print(feature.shape)

    path = np.load(pathPath)
    print(path)
    print(path.shape)
