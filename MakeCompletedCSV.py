import os
import pandas as pd

# Check Dataset Size
originTrainFilePath = './Dataset/NSMC/RawData/nsmc_train.txt'
spiltTrainDirPath = './Dataset/NSMC/Splited/train'
splitTrainFileList = os.listdir(spiltTrainDirPath)

originTestFilePath = './Dataset/NSMC/RawData/nsmc_test.txt'
splitTestDirPath = './Dataset/NSMC/Splited/test'
splitTestFileList = os.listdir(splitTestDirPath)
print(f'TRAIN, Split Files {len(splitTrainFileList)} -\n {splitTrainFileList}')
print(f'TEST, Split Files {len(splitTestFileList)} -\n {splitTestFileList}')

originTrainTables = pd.read_table(originTrainFilePath).dropna()
originTestTables = pd.read_table(originTestFilePath).dropna()

# Train
totalLineCount = 0
for splitTrainFile in splitTrainFileList:
    filePath = spiltTrainDirPath+'/'+splitTrainFile
    print(filePath)
    with open(spiltTrainDirPath+'/'+splitTrainFile, encoding='utf-8') as stf:
        for line in stf:
            totalLineCount += 1
print(f'TRAIN, Length -\n origin: {len(originTrainTables)}, split: {totalLineCount}')
print('Split OK!' if len(originTrainTables) == totalLineCount else 'ERROR - Split !' )

# Test
totalLineCount = 0
for splitTestFile in splitTestFileList:
    filePath = splitTestDirPath+'/'+splitTestFile
    print(filePath)
    with open(filePath, encoding='utf-8') as stf:
        for line in stf:
            totalLineCount += 1
print(f'TEST, Length -\n origin: {len(originTestTables)}, split: {totalLineCount}')
print('Split OK!' if len(originTestTables) == totalLineCount else 'ERROR - Split !' )

# Load Fixed Dataset
fixedDatasetPath = './Dataset/NSMC/Speller'
fixedDirList = os.listdir(fixedDatasetPath)
trainDirList = [file for file in fixedDirList if 'train_' in file]
testDirList = [file for file in fixedDirList if 'test_' in file]
print(f'TRAIN, DirSize: {len(trainDirList)} \n{trainDirList}')
print(f'TEST, DirSize: {len(testDirList)} \n{testDirList}')

# Grouping Fixed Dataset
print('\n -----Start Grouping Dataset !!!')
# Train
print('------TRAIN Dataset Grouping')
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
print(f'\n-----TRAIN Spller Dataset Size: {len(spllerTrainDataset)}')

#Test
print('------TEST Dataset Grouping')
spllerTestDataset = []
for dirIdx in range(0, len(testDirList)):
    idxPath = '/test_' + str(dirIdx)
    innerPath = fixedDatasetPath + idxPath
    repeatFile = '/before_test_doc_%s.txt.repeat' % str(dirIdx)
    curWorkingPath = innerPath+repeatFile
    print(f'\n--Current Working Path({os.path.exists(curWorkingPath)}): {curWorkingPath}')

    with open(curWorkingPath, mode='r', encoding='cp949') as rf:
        lines = rf.readlines()
        print(f'length of files: {len(lines)}')
        for line in lines:
            if '#Fixed:	' in line:
                fixedStr = line.split('#Fixed:	')[-1]
                spllerTestDataset.append(fixedStr)
    print(f'currSpeelerTrainSize: {len(spllerTestDataset)}')
print(f'\n-----TEST Spller Dataset Size: {len(spllerTestDataset)}')

# Connect with label
print('\n-----Start Grouping Dataset Connect with label')

trainLabelPath = './Dataset/NSMC/Splited/train_label.txt'
testLabelPath = './Dataset/NSMC/Splited/test_label.txt'
print(f'TRAIN label Path: {trainLabelPath}')
print(f'TEST label Path: {testLabelPath}')

trainLabelList = []
with open(trainLabelPath, mode='r', encoding='utf-8') as tlf:
    trainLabelList = tlf.readlines()
    print(f'TRAIN label Size: {len(trainLabelList)}')

trainPairSet = []
for idx in range(0, len(trainLabelList)):
    pair = (spllerTrainDataset[idx].strip(), trainLabelList[idx].strip())
    trainPairSet.append(pair)

# Test
testLabelList = []
with open(testLabelPath, mode='r', encoding='utf-8') as tlf:
    testLabelList = tlf.readlines()
    print(f'TEST label Size: {len(testLabelList)}')

testPairSet = []
for idx in range(0, len(testLabelList)):
    pair = (spllerTestDataset[idx].strip(), testLabelList[idx].strip())
    testPairSet.append(pair)    

# Make CSV
# Train
trainDict = {
    'document': [],
    'label': []
}
for idx, trainData in enumerate(trainPairSet):
    trainDict['document'].append(trainData[0])
    trainDict['label'].append(trainData[1])
trainCsvPath = './Dataset/NSMC/Completed/complete_train.csv'
trainDataFame = pd.DataFrame(trainDict)
trainDataFame.to_csv(trainCsvPath, sep=',', index=True, encoding='utf-8')
print(f'\n----TRAIN CSV Completed!! Path: {trainCsvPath}')

# Test
testDict = {
    'document': [],
    'label': []
}
for idx, testData in enumerate(testPairSet):
    testDict['document'].append(testData[0])
    testDict['label'].append(testData[1])
testCsvPath = './Dataset/NSMC/Completed/complete_test.csv'
testDataFame = pd.DataFrame(testDict)
testDataFame.to_csv(testCsvPath, sep=',', index=True, encoding='utf-8')
print(f'----TEST CSV Completed!! Path: {trainCsvPath}')
