import os
import re
import pandas as pd

# Check Dataset Size
originTrainFilePath = './Dataset/NSMC/RawData/nsmc_train.txt'
spiltTrainDirPath = './Dataset/NSMC/Splited/train'
splitTrainFileList = os.listdir(spiltTrainDirPath)
print(f'Train, Split Files {len(splitTrainFileList)} -\n {splitTrainFileList}')

origin_train_tables = pd.read_table(originTrainFilePath).dropna()

totalLineCount = 0
for splitTrainFile in splitTrainFileList:
    filePath = spiltTrainDirPath+'/'+splitTrainFile
    print(filePath)
    with open(spiltTrainDirPath+'/'+splitTrainFile, encoding='utf-8') as stf:
        for line in stf:
            totalLineCount += 1
print(f'Train, Length -\n origin: {len(origin_train_tables)}, split: {totalLineCount}')
print('Split OK!' if len(origin_train_tables) == totalLineCount else 'ERROR - Split !' )

# Load Fixed Dataset
fixedDatasetPath = './Dataset/NSMC/Speller'
fixedDirList = os.listdir(fixedDatasetPath)
trainDirList = [file for file in fixedDirList if 'train_' in file]
print(f'train, DirSize: {len(trainDirList)} \n{trainDirList}')

# Grouping Fixed Dataset
print('\n -----Start Grouping Dataset !!!')
spllerTrainDataset = []
for dirIdx in range(0, len(trainDirList)):
    idxPath = '/train_' + str(dirIdx)
    innerPath = fixedDatasetPath + idxPath
    repeatFile = '/before_train_doc_%s.txt.repeat' % str(dirIdx)
    curWorkingPath = innerPath+repeatFile
    print(f'\n--Current Working Path({os.path.exists(curWorkingPath)}): {curWorkingPath}')
    
    with open(curWorkingPath, mode='r', encoding='cp949') as rf:
        lines = rf.readlines()
        print(f'length of files: {len(lines)}')
        for line in lines:
            if '#Fixed:	' in line:
                fixedStr = line.split('#Fixed:	')[-1]
                spllerTrainDataset.append(fixedStr)
    print(f'currSpeelerTrainSize: {len(spllerTrainDataset)}')
    
print(f'\n-----Spller Dataset Size: {len(spllerTrainDataset)}')

# connect with label
print('\n-----Start Grouping Dataset Connect with label')

trainLabelPath = './Dataset/NSMC/Splited/train_label.txt'
print(f'Train label Path: {trainLabelPath}')

trainLabelList = []
with open(trainLabelPath, mode='r', encoding='utf-8') as tlf:
    trainLabelList = tlf.readlines()
    print(f'Train label Size: {len(trainLabelList)}')

trainPairSet = []
for idx in range(0, len(trainLabelList)):
    pair = (spllerTrainDataset[idx].strip(), trainLabelList[idx].strip())
    trainPairSet.append(pair)

# Make CSV
trainDict = {
    'document': [],
    'label': []
}
for idx, trainData in enumerate(trainPairSet):
    trainDict['document'].append(trainData[0])
    trainDict['label'].append(trainData[1])
trainCsvPath = './Dataset/NSMC/Completed/complete_train.csv'
trainDataFame = pd.DataFrame(trainDict)
trainDataFame.to_csv(trainCsvPath, sep=',', 
                        index=True)
print(f'\n----Completed!! Path: {trainCsvPath}')