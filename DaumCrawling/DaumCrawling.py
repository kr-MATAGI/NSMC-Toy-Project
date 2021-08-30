from sys import is_finalizing
from selenium import webdriver

import time
import pandas as pd

# def
DAUM_RAW_SAVED_PATH = './Dataset/Daum_Movie/RawData'

# Pause Time
WAIT_TIME = 3
PAUSE_TIME = 0.7
CLICK_TIME = 0.5

class DaumCrawler:
    __driverPath = None
    __driver = None
    __reivewUrl = 'https://movie.daum.net/moviedb/grade?movieId=%s&type=netizen&page=1'

    '''
        Initalizer
        Set Deriver Path
    '''
    def __init__(self, driverPath):
        print('[Config] Set WebDriver Path: ', driverPath)
        self.__driverPath = driverPath

        try:
            self.__driver = webdriver.Chrome(self.__driverPath)
            self.__driver.implicitly_wait(WAIT_TIME)
        except Exception as e:
            print('ERROR - Set Webdriver: ', e)

    '''
        Daum movie review Crawling
    '''
    def DaumMovieCraling(self, url, movieId):
        startTime = time.time()

        # Access Movie Review Page
        self.__driver.get(url)

        # Click More Comment Btn
        isClickedMoreBtn = False
        while True:
            try:
                moreBtn = self.__driver.find_element_by_xpath('//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button/span[2]')
                moreBtn.click()
                time.sleep(CLICK_TIME)
                isClickedMoreBtn = True
            except:
                print('Finished - Click more btn')
                break
        
        # Parsing
        isParsed = False
        if True == isClickedMoreBtn:
            #Extreact User's Movie Comments
            reviewList = []

            try:
                commentsClass = self.__driver.find_element_by_class_name('list_comment')
                commentLi = commentsClass.find_elements_by_tag_name('li')

                for liItem in commentLi:
                    try:
                        cmtInfo = liItem.find_element_by_class_name('cmt_info')

                        # Get Review
                        descTxt = cmtInfo.find_element_by_class_name('desc_txt')
                        review = descTxt.text
                        review = review.replace('\n', ' ')
                        
                        # Get Star Score
                        ratings = cmtInfo.find_element_by_class_name('ratings')
                        score = ratings.text
                        #print(f'Score: {score}, Review: {review}')
                    except Exception as e:
                        print('ERROR -', e)
                        continue
                
                    reviewPair = (score, review)
                    reviewList.append(reviewPair)
                isParsed = True

            except Exception as e:
                print('ERROR -', e)

        if True == isParsed:
            print('\n --- START WRITE FILE ---')

            # Convert to Dict & Make labeles
            dataDict = {
                'document': [],
                'score': [],
                'label': []
            }

            for reviewPair in reviewList:
                label = 1 if 5 <= int(reviewPair[0]) else 0
                dataDict['document'].append(reviewPair[1])
                dataDict['score'].append(reviewPair[0])
                dataDict['label'].append(label)

            fileName = '/Daum_%s_review.csv' % str(movieId)
            print('Write Size: ', len(reviewList))
            print('saved path: ', DAUM_RAW_SAVED_PATH+fileName)
            
            dataFame = pd.DataFrame(dataDict)
            dataFame.to_csv(DAUM_RAW_SAVED_PATH+fileName, 
                            sep='\t', 
                            index=True)
        else: print('ERROR - Parsing Process !')
        print('Processing Time: ', time.time() - startTime)


    '''
        Start Auto Crawling by loop
    '''
    def AutoCrawling(self, LoopCount=0):
        startTime = time.time()
        
        for lc in range(1, LoopCount):
            time.sleep(PAUSE_TIME)

            movieId = lc
            movieUrl = (self.__reivewUrl) % movieId
            print('Current URL:', movieUrl)

            self.DaumMovieCraling(movieUrl, movieId)
        
        print('Total Time: ', time.time() - startTime)

    '''
        Start Manual Crawling by movie ID
    '''
    def InsertMovieIdCrawling(self, movieId):
        time.sleep(PAUSE_TIME)

        movieUrl = (self.__reivewUrl) % movieId
        print('Current URL:', movieUrl)
        
        self.DaumMovieCraling(movieUrl, movieId)