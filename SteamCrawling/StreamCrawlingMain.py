from SteamReivewParser import SteamReviewParser
import time

'''
    Crawling Stream Game Review
'''

# init
startTime = time.time()
parser = SteamReviewParser('chromedriver.exe')

'''
# Scrolling
parser.GetTopSellerGames(10)

# Parsing id, name
gameList = parser.ParsingGamesInfo()

# Get Review and Write CSV
parser.WriteGameReviewToCSV(100, gameList)

print('\n----All Task End... Total Time: ', time.time()-startTime)
'''

'''
    Merge Game Review
'''
#parser.MergeAllRawDataset()

'''
    Splite Train and Test Dataset
'''
parser.SpliteTrainAndTest(0.2, 2021)