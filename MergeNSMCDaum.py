import os
import pandas as pd

# Path
nsmcTrainPath = './Dataset/NSMC/RawData/nsmc_train.txt'
nsmcTestPath = './Dataset/NSMC/Completed/complete_test.csv'

daumTrainpath = './Dataset/Daum_Movie/Completed/daum_train.tsv'
daumTestpath = './Dataset/Daum_Movie/Completed/daum_test.tsv'

# Table
nsmcTrainTable = pd.read_table(nsmcTrainPath, encoding='UTF-8')
nsmcTestTable = pd.read_csv(nsmcTestPath, 'r', encoding='UTF-8', delimiter=',')

daumTrainTable = pd.read_csv(daumTrainpath, 'r', encoding='UTF-8', delimiter='\t')
daumTestTable = pd.read_csv(daumTestpath, 'r', encoding='UTF-8', delimiter='\t')

# Merge
#Train
mergedTrainTable = pd.concat([nsmcTrainTable, daumTrainTable])
mergedTestTable = pd.concat([nsmcTestTable, daumTestTable])

# Write
WriteTrainPath = './Dataset/NSMC/Completed/nsmc_and_daum_train.tsv'
WriteTestPath = './Dataset/NSMC/Completed/nsmc_and_daum_test.tsv'

mergedTrainTable = mergedTrainTable.sample(frac=1)
mergedTestTable = mergedTestTable.sample(frac=1)

mergedTrainTable.to_csv(WriteTrainPath, sep='\t', index=False, encoding='utf-8')
mergedTestTable.to_csv(WriteTestPath, sep='\t', index=False, encoding='utf-8')
print(len(mergedTrainTable), len(mergedTrainTable) == (len(nsmcTrainTable) + len(daumTrainTable)))
print(len(mergedTestTable), len(mergedTestTable) == (len(nsmcTestTable) + len(daumTestTable)))