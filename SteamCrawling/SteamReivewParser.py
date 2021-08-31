from selenium import webdriver
from sklearn.model_selection import train_test_split

import time
import os
import pandas as pd
import re

# Def
GAME_LIST_URL = 'http://store.steampowered.com/search/?filter=topsellers&l=korean'
REVIEW_BASE_URL = 'http://steamcommunity.com/app/%s/reviews/?filterLanguage=koreana&p=1&browsefilter=toprated'
RAWDATA_PATH = './Dataset/Steam/RawData'
MERGED_PATH = './Dataset/Steam/Merged'
SPLITED_PATH = './Dataset/Steam/Splited'
PAUSE_TIME = 1

# Script
script = {
    'GET_SCROLL_HEIGHT': 'return document.body.scrollHeight',
    'SCROLL_DOWN': 'window.scrollTo(0, document.body.scrollHeight);'
}

class SteamReviewParser:
    __driverPath = ''
    __driver = None

    '''
        Initialize
    '''
    def __init__(self, driverPath):
        print('[Config] Set Webdriver Path: ', driverPath)
        self.__driverPath = driverPath

        try:
            self.__driver = webdriver.Chrome(self.__driverPath)
            self.__driver.implicitly_wait(3)
        except Exception as e:
            print('ERROR - Set Webdriver: ', e)

    '''
        Scrolling a current Page
    '''
    def GetTopSellerGames(self, scrollDownCnt):
        # Init Config
        startTime = time.time() 
        self.__driver.get(GAME_LIST_URL)

        # Scroll down
        scrollHeight = self.__driver.execute_script(script['GET_SCROLL_HEIGHT'])
        print('Scroll Height -', scrollHeight)

        for cnt in range(scrollDownCnt):
            print('Scroll Down Count: ', cnt+1)
            
            try:
                self.__driver.execute_script(script['SCROLL_DOWN'])
            except Exception as e:
                print('ERROR - First Scroll Down Cmd: ', e)

            # Wait Loading
            time.sleep(PAUSE_TIME)

            # Get New Scroll Height
            try:
                newScrollHeight = self.__driver.execute_script(script['GET_SCROLL_HEIGHT'])
                if newScrollHeight == scrollHeight: break
                else: scrollHeight = newScrollHeight
            except Exception as e:
                print('ERROR - Loop Get Scroll Height Cmd: ', e)

        print('\n-----End Scroll Down, Processing Time: ', time.time() - startTime)

    '''
        Parsing Game appid, name
    '''    
    def ParsingGamesInfo(self):
        retValList = [] # [(Game Name, Game Id)]

        # Init Config
        startTime = time.time()

        # Parsing Game
        searchResultsRows = None
        try:
            searchResultsRows = self.__driver.find_elements_by_class_name('search_result_row')
            print('Success - Get search_resultsRows, Len:', len(searchResultsRows))
        except Exception as e:
            print('ERROR - Get by id(search_resultsRows) ', e)
        
        for item in searchResultsRows:
            try:
                appid = item.get_attribute('data-ds-appid')
                resSearchCombined = item.find_element_by_class_name('responsive_search_name_combined')
                ellipsis = resSearchCombined.find_element_by_class_name('ellipsis')
                gameName = ellipsis.find_element_by_class_name('title').text
                
                if (None != appid) and (0 < len(gameName)): retValList.append((appid, gameName))                
            except Exception as e:
                print(e)

        print('\n----End Parsing Games Info, Processing Time: ', time.time() - startTime)
        return retValList


    '''
        Write Game Review to CSV
    '''
    def WriteGameReviewToCSV(self, scrollCnt, gameList):
        # config
        startTime = time.time()
        regex = re.compile('[a-zA-Z0-9]*')
        
        # Get Review
        for gameInfo in gameList:
            reviewPairList = []

            gameId = gameInfo[0]
            gameName = re.sub(r"[^a-zA-Z0-9]","", gameInfo[1]).replace(' ', '_')
            print(f'current processing game - id: {gameId}, name: {gameName}')

            targetUrl = REVIEW_BASE_URL % str(gameId)
            self.__driver.get(targetUrl)
            time.sleep(PAUSE_TIME)
            
            # Check Adult Game
            try:
                self.__driver.find_element_by_id('ViewAllForApp').click()
                self.__driver.find_element_by_id('age_gate_btn_continue').click()
                print('Access Adult Game!')
                time.sleep(PAUSE_TIME)
            except Exception as e:
                print('Not ERROR - Not Adult Game... - ', e)

            # Scrolling
            scrollHeight = self.__driver.execute_script(script['GET_SCROLL_HEIGHT'])
            print('Scroll Height -', scrollHeight)
            for scIdx in range(scrollCnt):
                try:
                    self.__driver.execute_script(script['SCROLL_DOWN'])
                    print('Exec Scroll Down !')
                except Exception as e:
                    print('ERROR - First Scroll Down Cmd: ', e)

                # Wait Loading
                time.sleep(PAUSE_TIME)
                
                try:
                    newScrollHeight = self.__driver.execute_script(script['GET_SCROLL_HEIGHT'])
                    if newScrollHeight == scrollHeight: break
                    else: scrollHeight = newScrollHeight
                except Exception as e:
                    print('ERROR - Loop Get Scroll Height Cmd: ', e)

            # Get Reviews
            UserReviewCardContent = None
            voteHeader = None

            try:
                UserReviewCardContent = self.__driver.find_elements_by_class_name('apphub_UserReviewCardContent')
                print('UserReviewCardContent Len: ', len(UserReviewCardContent))
            except Exception as e:
                print('ERROR - Get apphubCardTextContent, ', e)

            for cardContent in UserReviewCardContent:
                sementic = None
                sentence = None

                try:
                    voteHeader = cardContent.find_element_by_class_name('vote_header')
                    reviewInfo = voteHeader.find_element_by_class_name('reviewInfo')
                    title = reviewInfo.find_element_by_class_name('title')
                    if 'Recommended' == title.text: sementic = 1
                    else: sementic = 0
                except Exception as e:
                    print('ERROR - Get voteHeader, ', e)

                try:
                    reviewStr = cardContent.find_element_by_class_name('apphub_CardTextContent')
                    sentence = [ data for data in reviewStr.text.split('\n') if '<div' not in data]
                                        
                    # Extract Review Sentence
                    sentence = ' '.join(sentence)
                    hangulEngReg = re.compile('[^ ㄱ-ㅣ가-힣]+')
                    sentence = hangulEngReg.sub('', sentence)
                    sentence = sentence.strip()

                except Exception as e:
                    print('ERROR - Get UserReviewCardContent, ', e)
                
                if None != sementic and None != sentence: reviewPairList.append((sentence, sementic))
            if 0 < len(reviewPairList):
                reviewDict = {
                    'document': [],
                    'label': []
                }
                for reviewData in reviewPairList:
                    reviewDict['document'].append(reviewData[0])
                    reviewDict['label'].append(reviewData[1])
                
                # Write CSV
                fileName = ('/Steam_%s_review.csv') % str(gameName)
                print('Write Size: ', len(reviewPairList))
                print('saved path: ', RAWDATA_PATH+fileName)

                reviewFrame = pd.DataFrame(reviewDict)
                reviewFrame.to_csv(RAWDATA_PATH+fileName, sep='\t', index=True)
            else:
                print(f'{gameName} Review List is Empty')
            
            # break
            time.sleep(PAUSE_TIME)
        print('\nb----End Write Review, Processing Time:', time.time() - startTime)

    '''
        Merge All Raw Dataset
    '''
    def MergeAllRawDataset(self):
            datasetFileList = os.listdir(RAWDATA_PATH)
            print('All Dataset Count: ', len(datasetFileList))
            print(datasetFileList)

            # Merge
            destFrame = None
            for idx, fileName in enumerate(datasetFileList):
                fullPath = RAWDATA_PATH + '/' + fileName
                dataFrame = pd.read_csv(fullPath, sep='\t', encoding='UTF-8').dropna()
                
                if 0 == idx: destFrame = dataFrame
                else: destFrame = pd.concat([destFrame, dataFrame])
            print('Merged Len - ', len(destFrame))

            # Write TSV
            destFullPath = MERGED_PATH + '/' + 'Merged_Steam_review.tsv'
            destFrame.to_csv(destFullPath, sep='\t', encoding='UTF-8', index=False, header=['id', 'document', 'label'])
            print('--Finished, Merge Steam Game Review !')

    '''
        Splite Train / Test Dataset from merged dataset
    '''
    def SpliteTrainAndTest(self, testRatio=0.2, rndSeed=2021):
        mergedFilePath = MERGED_PATH + '/' + 'Merged_Steam_review.tsv'
        trainTargetPath = SPLITED_PATH + '/' + 'train_steam.tsv'
        testTargetPath = SPLITED_PATH + '/' + 'test_steam.tsv'

        mergedDataFrame = pd.read_csv(mergedFilePath, sep='\t', encoding='UTF-8')
        mergedDoc = mergedDataFrame['document']
        mergedLabel = mergedDataFrame['label']

        x_train, x_test, y_train, y_test = train_test_split(mergedDoc, mergedLabel, test_size=testRatio, shuffle=True,
                                                            stratify=mergedLabel, random_state=rndSeed)
        
        trainDataset = pd.DataFrame({'document': x_train, 'label': y_train})
        testDataset = pd.DataFrame({'document': x_test, 'label': y_test})
        
        trainDataset.to_csv(trainTargetPath, sep='\t', encoding='UTF-8', index=True)
        testDataset.to_csv(testTargetPath, sep='\t', encoding='UTF-8', index=True)

        print(f'---End Split Train{len(trainDataset)} / Test Dataset{len(testDataset)}')

        

        