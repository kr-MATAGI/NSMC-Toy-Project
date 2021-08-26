import os
import csv
import math
import pandas as pd
from sklearn.model_selection import train_test_split

# Global Def
testRatio = 0.3 # 7 : 3 (train : test)
validRatio = 0.2 # 8 : 2 (train : valid)
RND_STATE = 2021

# Load updated_daum_review.csv
originFilePath = './Dataset/Daum_Movie/Merged/updated_daum_review.csv'

# Divide Train and Test Dataset
trainDoc = []
trainLabel = []
testDoc = []
testLabel = []
mergedDoc = []
mergedLabel = []
originTableSize = 0
with open(originFilePath, 'r', encoding='UTF-8') as originFile:
    originTable = pd.read_csv(originFilePath)
    originTableSize = len(originTable)
    print(f'originTableSize: {originTableSize}')

    docDataset = originTable['document']
    labelDataset = originTable['label']

    trainDoc, testDoc, trainLabel, testLabel = train_test_split(docDataset, labelDataset,
                                                                test_size=testRatio,
                                                                shuffle=True,
                                                                stratify=labelDataset,
                                                                random_state=RND_STATE)
    print(f'TRAIN Len - doc: {len(trainDoc)}, label: {len(trainLabel)}')
    print(f'TEST Len - doc: {len(testDoc)}, label: {len(testLabel)}')

print(f'train + valid == trainDataset: {len(trainDoc) + len(testDoc) == originTableSize}')

# Write TSV files
writeDirPath = './Dataset/Daum_Movie/Completed'
trainFileName = 'daum_train.tsv'
testFileName = 'daum_test.tsv'
mergedFileName = 'daum_merged.tsv'

# Train
TrainDataFame = pd.DataFrame({'document': trainDoc, 'label': trainLabel})
TrainDataFame.to_csv(writeDirPath + '/' + trainFileName, sep='\t', index=True, encoding='utf-8')

# Test
TestDataFame = pd.DataFrame({'document': testDoc, 'label': testLabel})
TestDataFame.to_csv(writeDirPath + '/' + testFileName, sep='\t', index=True, encoding='utf-8')

print('\n-------Finish, Check Path - ', writeDirPath)


# Merged Set
mergedDataFrame = pd.concat([TrainDataFame, TestDataFame])
mergedDataFrame.to_csv(writeDirPath + '/' + mergedFileName, sep='\t', index=True, encoding='utf-8')
print(f'Len same ? - {len(mergedDataFrame) == originTableSize}')