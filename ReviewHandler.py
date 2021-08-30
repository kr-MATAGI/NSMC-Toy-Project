import pandas as pd
import urllib.request
import os

# def
# NSMC Splite Size
NSMCSplitSize = 10000

# NSMC Type
NSMCType = {
    'TRAIN': 0,
    'TEST': 1
}

# Donwload URL
NSMCDownloadUrl = 'https://raw.githubusercontent.com/e9t/nsmc/master/'

# Path
RawDataDirPath = {
    'DAUM': './Dataset/Daum_Movie/RawData',
    'NAVER': './Dataset/NSMC/RawData',
}

NSMCSpellerDirPath = './Dataset/NSMC/Speller'
NSMCCompletedDirPath = './Dataset/NSMC/Completed'
NSMCSplitedDirPath = './Dataset/NSMC/Splited'

# Daum Movie Review
DaumMergedDirPath = './Dataset/DaumMovie/Merged'
DaumCompletedDirPath = './Dataset/DaumMovie/Completed'

class ReviewHandler:
    
    '''
        Merged Daum Review
    '''
    def MergeDaumRawDataFiles(self):
        # Load file list
        parentDirPath = RawDataDirPath['DAUM']

        rawDataFiles = os.listdir(parentDirPath)
        print(f'----Daum Movie Review Data Path: {parentDirPath}')
        print(f'Size: {len(rawDataFiles)}, \nFile List: \n{rawDataFiles}')

        # Merge
        print('\n----Start File Contents Merging')

        dataPairList = []
        for fileName in rawDataFiles:
            print(f'Currnet Processing File: ', fileName)
            
            fullFilePath = parentDirPath + '/' + fileName
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

            # Write CSV Files
            csvDict = {
                'document': [],
                'score': [],
                'label': []
            }

            for dataPair in dataPairList:
                csvDict['document'].append(dataPair[0])
                csvDict['score'].append(dataPair[1])
                csvDict['label'].append(dataPair[2])

            csvFilePath = DaumMergedDirPath + '/' + 'merged_daum_review.tsv'
            mergedDataFrame = pd.DataFrame(csvDict)
            mergedDataFrame.to_csv(csvFilePath, sep='\t', index=True, encoding='UTF-8')
            print(f'----Make CSV Completed!! Path: {csvFilePath}')

    '''
        Splite NSMC 'document' column
        @Param
            type: 0 - train, 1 - test
            colName: Target Column
    '''
    def SpliteRawDataNSMC(self, srcData, type=0, colName='document'):
        rawDataPath = RawDataDirPath['NAVER']
        if NSMCType['TRAIN'] == type: rawDataPath += '/nsmc_train.txt'
        else: rawDataPath += '/nsmc_test.txt'

        # Read Table    
        nsmcRawTable = pd.read_table(rawDataPath).dropna()
        print(f'NSMC type:{type}, Table Size: {len(nsmcRawTable)}')

        # Make Splited File
        destFilePath = NSMCSplitedDirPath
        if 'document' == colName: 
            destFilePath += '/train'

            if NSMCType['TRAIN'] == type: destFilePath += '/before_train_doc_'
            else: destFilePath += '/before_test_doc_'

        if 'label' == colName:
            if NSMCType['TRAIN'] == type: destFilePath += '/train_label.txt'
            else: destFilePath += '/test_label.txt'

        if 'document' == colName:
            totalLoopStep = int(len(srcData) / NSMCSplitSize)
            for idx in range(totalLoopStep):
                startIdx = idx * NSMCSplitSize
                endIdx = idx  * NSMCSplitSize + NSMCSplitSize

                writeList = []
                if idx == totalLoopStep - 1: writeList = srcData[startIdx:]
                else: writeList = srcData[startIdx:endIdx]

                destFilePath += (str(idx) + '.txt')
                with open(destFilePath, mode='w', encoding='utf-8') as f:
                    writeCnt = 0
                    for idx, data in enumerate(writeList):
                        try:
                            f.write(data + '\n')
                            writeCnt += 1
                        except Exception as e:
                            print(idx, data, e)
                    print(f'origin: {len(nsmcRawTable)}, write: {writeCnt}')
        else:
            with open(destFilePath, mode='w', encoding='utf-8') as f:
                writeCnt = 0
                for idx, data in enumerate(srcData):
                    try:
                        f.write(str(data) + '\n')
                        writeCnt += 1
                    except Exception as e:
                        print(idx, data, e)
                print(f'origin: {len(nsmcRawTable)}, write: {writeCnt}')

    '''
        Download NSMC Raw Dataset
    '''
    def DownloadNSMCDataset(self):
        # Config Path
        TrainDatasetUrl = NSMCDownloadUrl + '/ratings_train.txt'
        TestDatasetUrl = NSMCDownloadUrl + '/ratings_test.txt'

        TrainSavePath = RawDataDirPath['NAVER'] + '/nsmc_train.txt'
        TestSavePath = RawDataDirPath['NAVER'] + '/nsmc_test.txt'

        # Download
        try:
            urllib.request.urlretrieve(TrainDatasetUrl, filename=TrainSavePath)
            urllib.request.urlretrieve(TestDatasetUrl, filename=TestSavePath)
            print('Finished NSMC Raw Dataset Download !')
        except Exception as e:
            print('ERROR - Download NSMC Raw Dataset, ', e)

 
    '''
        Merge CSV Files
    '''
    def MergeCsvDataset(self, srcPath_1, srcPath_2, destPath):
        # Check and Config
        print('\n----Start Merge CSV Files')
        print('path_1:', srcPath_1)
        print('path_2:', srcPath_2)

        # Read
        srcTable_1 = pd.read_csv(srcPath_1, sep='\t', encoding='UTF-8')
        srcTable_2 = pd.read_csv(srcPath_2, sep='\t', encoding='UTF-8')
        print(f'Checking Len - src_1: {len(srcTable_1)}, src_2: {len(srcTable_2)}')

        # Concat Table
        mergedTable = pd.concat([srcTable_1, srcTable_2])
        
        # Shuffle
        mergedTable = mergedTable.sample(frac=1)

        mergedTable.to_csv(destPath, sep='\t', index=False, encoding='UTF-8')
        print(f'Checking Len - mergedTable: {len(mergedTable)}, srcTables: {len(srcTable_1)}, {srcTable_2}')

