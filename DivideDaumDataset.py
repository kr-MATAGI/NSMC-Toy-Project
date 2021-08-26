import os
import csv
import math
import pandas as pd
from sklearn.model_selection import train_test_split

# Global Def
trainRatio = 0.7 # 7 : 3 (train : test)
validRatio = 0.2 # 8 : 2 (train : valid)
RND_STATE = 2021

# Load updated_daum_review.csv
originFilePath = './Dataset/Daum_Movie/Merged/updated_daum_review.csv'

# Divide Train and Test Dataset
trainDataset = []
testDataset = []
with open(originFilePath, 'r', encoding='UTF-8') as originFile:
    originTable = pd.read_csv(originFilePath)
    originTableSize = len(originTable)
    print(f'originTableSize: {originTableSize}')

    originDoc = originTable['document']
    originLabel = originTable['label']

    trainLastIndex = math.floor((len(originDoc) * trainRatio))
    trainDataset = originTable[:trainLastIndex]
    testDataset = originTable[trainLastIndex:]
    print('\n-------TRAIN Dataset:')
    print(trainDataset)
    print('\n-------TEST Dataset:')
    print(testDataset)

    print(f'\n origingSize == TRAIN + TEST: { originTableSize == (len(trainDataset) + len(testDataset))}')

# Divide Train and Valid Dataset - Not Needed
'''
trainDoc = trainDataset['document']
trainLabel = trainDataset['label']
x_train, x_valid, y_train, y_valid = train_test_split(trainDoc, trainLabel, 
                                                    test_size=validRatio,
                                                    shuffle=True,
                                                    stratify=trainLabel,
                                                    random_state=RND_STATE)

print(f'train + valid == trainDataset: {len(x_train) + len(x_valid) == len(trainDataset)}')
'''

# Write TSV files
writeDirPath = './Dataset/Daum_Movie/Completed'
trainFileName = 'daum_train.tsv'
testFileName = 'daum_test.tsv'

# Train
writerDataFame = pd.DataFrame(trainDataset)
writerDataFame.to_csv(writeDirPath + '/' + trainFileName, sep='\t', index=False, encoding='utf-8')

# Test
writerDataFame = pd.DataFrame(testDataset)
writerDataFame.to_csv(writeDirPath + '/' + testFileName, sep='\t', index=False, encoding='utf-8')

print('\n-------Finish, Check Path - ', writeDirPath)

#test = pd.read_csv('./Dataset/Daum_Movie/Completed/daum_test.tsv', delimiter='\t')
#print(test)