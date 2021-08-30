from selenium import webdriver

import time
import pandas as pd
import re

# Def
GAME_LIST_URL = 'http://store.steampowered.com/search/?filter=topsellers&l=korean'
REVIEW_BASE_URL = 'http://steamcommunity.com/app/%s/reviews/?filterLanguage=koreana'
SAVED_PATH = './SteamCrawling/Review'
PAUSE_TIME = 0.6

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
                print('saved path: ', SAVED_PATH+fileName)

                reviewFrame = pd.DataFrame(reviewDict)
                reviewFrame.to_csv(SAVED_PATH+fileName, sep='\t', index=True)
            else:
                print(f'{gameName} Review List is Empty')
            
            # break
            time.sleep(PAUSE_TIME)
        print('\nb----End Write Review, Processing Time:', time.time() - startTime)

