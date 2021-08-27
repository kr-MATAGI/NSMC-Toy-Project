from selenium import webdriver
import time
import pandas as pd

SAVED_PATH = './Dataset/Daum_Movie'

WAIT_TIME = 3
PAUSE_TIME = 2
CLICK_TIME = 0.5

# Set Chrome Driver
driverPath = './chromedriver.exe'
driver = webdriver.Chrome(driverPath)
driver.implicitly_wait(3)

# Loop
LoopCount = 10000
for lc in range(1, LoopCount):
    startTime = time.time()

    time.sleep(PAUSE_TIME)

    # Configuration
    print('영화 이름은 띄어쓰기 없이')
    print('영화의 이름, id를 입력(예, 인질 127738): ')
    movieId = lc

    movieUrl = 'https://movie.daum.net/moviedb/grade?movieId=%s&type=netizen&page=1' % str(lc)
    print('URL: ', movieUrl)

    # Access Web Page
    driver.get(movieUrl)
    
    # Clcik more comment
    isAllList = False
    while True:
        try:
            moreBtn = driver.find_element_by_xpath('//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button/span[2]')
            moreBtn.click()
            time.sleep(CLICK_TIME)
            isAllList = True
        except:
            print('ERROR - Click "more Btn"')
            break
    
    isParsred = False
    if True == isAllList:
    # Extract User's Comments
        reviewList = []
        try:
            commentsClass = driver.find_element_by_class_name('list_comment')
            commentLi = commentsClass.find_elements_by_tag_name('li')
            
            for item in commentLi:
                try:
                    cmtInfo = item.find_element_by_class_name('cmt_info')
                    
                    # review
                    descTxt = cmtInfo.find_element_by_class_name('desc_txt')
                    review = descTxt.text
                    review = review.replace('\n', ' ')

                    # star score
                    ratings = cmtInfo.find_element_by_class_name('ratings')
                    score = ratings.text
                    #print(f'Score: {score}, Review: {review}')
                except Exception as e:
                    print('ERROR - \n', e)
                    continue

                reviewPair = (score, review)
                reviewList.append(reviewPair)
            isParsred = True
            #print(reviewList)
        
        except Exception as e:
            print('ERROR - \n', e)

    if True == isParsred:
        print('\n --- START WRITE FILE ---')
        
        # Convert to Dict & Make labeles
        dataDict = {'document': [],
                    'score': [],
                    'label': []}
        for reviewPair in reviewList:
            label = 1 if 6 <= int(reviewPair[0]) else 0
            dataDict['document'].append(reviewPair[1])
            dataDict['score'].append(reviewPair[0])
            dataDict['label'].append(label)

        fileName = '/Daum_%s_review.csv' % str(movieId)
        print('Write Size: ', len(reviewList))
        print('saved path: ', SAVED_PATH+fileName)

        dataFame = pd.DataFrame(dataDict)
        dataFame.to_csv(SAVED_PATH+fileName, sep='\t', 
                        index=True)

    else: print('ERROR - Parsing Process !')

    print('Processing Time: ', time.time() - startTime)