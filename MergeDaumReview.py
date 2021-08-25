import os
import pandas as pd

reviewDirPath = './Dataset/Daum_Movie/Review'
reviewFileList = os.listdir(reviewDirPath)
print(f'----Daum Movie Review Data Path: {reviewDirPath}')
print(f'Size: {len(reviewFileList)}, \nFile List: \n{reviewFileList}')

# Merge review files
print('\n-----Start File Contents Merging')

dataPairList = []
for fileName in reviewFileList:
    print(f'Currnet Processing File: ', fileName)

    fullFilePath = reviewDirPath + '/' + fileName
    csvTable = pd.read_csv(fullFilePath, encoding='utf-8')
    print(f'Contents Size: {len(csvTable)}')

    docDataList = csvTable['document']
    scoreDataList = csvTable['score']
    labelDataList = csvTable['label']
    
    for idx in range(len(csvTable)):
        docData = docDataList[idx]
        score = scoreDataList[idx]
        label = labelDataList[idx]
        dataTriPair = (docData, score, label)
        dataPairList.append(dataTriPair)
print(f'\n----Total Contents Size: {len(dataPairList)}')

# Wrtie CSV File
csvDict = {
    'document': [],
    'score': [],
    'label': []
}

for dataPair in dataPairList:
    csvDict['document'].append(dataPair[0])
    csvDict['score'].append(dataPair[1])
    csvDict['label'].append(dataPair[2])
mergedCsvPath = './Dataset/Daum_Movie/Merged/merged_daum_review.csv'
mergedDataFame = pd.DataFrame(csvDict)
mergedDataFame.to_csv(mergedCsvPath, sep=',', index=True, encoding='utf-8')
print(f'----Make CSV Completed!! Path: {mergedCsvPath}')