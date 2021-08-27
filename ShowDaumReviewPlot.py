from os import sep
import matplotlib.pyplot as plt
import pandas as pd

# 0 ~ 10 star score
updatedDaumReviewPath = './Dataset/NSMC/Completed/nsmc_and_daum_test.tsv'
daumReviewTable = pd.read_csv(updatedDaumReviewPath, encoding='utf-8', sep='\t')
print(daumReviewTable)

#scoreTable = daumReviewTable['score']
#starScoreList = scoreTable.to_list()

labelTable = daumReviewTable['label']
labelList = labelTable.to_list()

# Show score plt
#plt.hist(scoreTable.to_list())
#plt.title("Daum movie review score's hist")
#plt.xlabel('score')
#plt.ylabel('num of samples')
#plt.show()

# show label plt
plt.hist(labelTable.to_list())
plt.title("NSMC and Daum Test Dataset")
plt.xlabel('label')
plt.ylabel('num of samples')
plt.show()