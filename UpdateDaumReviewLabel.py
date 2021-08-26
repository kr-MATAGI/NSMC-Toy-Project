import pandas as pd

# Input
daumReviewFilePath = './Dataset/Daum_Movie/Merged/merged_daum_review.csv'
daumReviewTable = pd.read_csv(daumReviewFilePath, encoding='utf-8')
prevUpdateLen = len(daumReviewTable)
print('Review Size: ', prevUpdateLen)

docDataList = daumReviewTable['document']
scoreDataList = daumReviewTable['score']
labelDataList = daumReviewTable['label']

# Update
negCriteria = 4

updateDict = {
    'document': [],
    'score': [],
    'label': []
}
for idx in range(prevUpdateLen):
    updateDict['document'].append(docDataList[idx])
    updateDict['score'].append(scoreDataList[idx])
    
    newLabel = '0' if negCriteria >= int(scoreDataList[idx]) else '1'
    #if newLabel != labelDataList[idx]: print(f'{docDataList[idx]} {scoreDataList[idx]} {labelDataList[idx]} to {newLabel}')
    updateDict['label'].append(newLabel)

# Write CSV
updateCSVPath = './Dataset/Daum_Movie/Merged/updated_daum_review.csv'
updatedDataFame = pd.DataFrame(updateDict)
updatedDataFame.to_csv(updateCSVPath, sep=',', index=True, encoding='utf-8')

afterUpdateLen = len(updatedDataFame)
print(f'Length is Same? - {prevUpdateLen == afterUpdateLen}')
print(f'prev: {prevUpdateLen}, after: {afterUpdateLen}')
print(f'----Make CSV Completed!! Path: {updateCSVPath}')
