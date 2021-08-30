from SteamReivewParser import SteamReviewParser
import time

# init
startTime = time.time()
parser = SteamReviewParser('chromedriver.exe')

# Scrolling
parser.GetTopSellerGames(1)

# Parsing id, name
gameList = parser.ParsingGamesInfo()

# Get Review and Write CSV
parser.WriteGameReviewToCSV(1, gameList)

print('\n----All Task End... Total Time: ', time.time()-startTime)