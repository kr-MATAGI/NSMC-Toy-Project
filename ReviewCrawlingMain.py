from ReviewHandler import ReviewHandler

# Init
reviewHandler = ReviewHandler()

# Make Merged Dataset

'''
    Speller NSMC + Daum Review
'''
# 1.1   train - speller nsmc + daum
path_1_csv = './Dataset/NSMC/Completed/complete_train.csv'
path_1_tsv = './Dataset/NSMC/Completed/complete_train.tsv'
#reviewHandler.ConvertCsv2Tsv(path_1_csv, path_1_tsv)

path_2 = './Dataset/DaumMovie/Completed/daum_train.tsv'
destPath = './Dataset/MergedDataset/Train_SpellerNSMC_Daum.tsv'
#reviewHandler.MergeTsvDataset(path_1_tsv, path_2, destPath)

# 1.2   test - speller nsmc + daum
path_1_csv = './Dataset/NSMC/Completed/complete_test.csv'
path_1_tsv = './Dataset/NSMC/Completed/complete_test.tsv'
#reviewHandler.ConvertCsv2Tsv(path_1_csv, path_1_tsv)

path_2 = './Dataset/DaumMovie/Completed/daum_test.tsv'
destPath = './Dataset/MergedDataset/Test_SpellerNSMC_Daum.tsv'
#reviewHandler.MergeTsvDataset(path_1_tsv, path_2, destPath)


'''
    NSMC + Daum Review
'''
# 2.1   Train - Raw NSMC + daum
path_1_txt = './Dataset/NSMC/RawData/nsmc_train.txt'
path_1_tsv = './Dataset/NSMC/RawData/nsmc_train.tsv'
# reviewHandler.ConvertText2Tsv(path_1_txt, path_1_tsv)

path_2 = './Dataset/DaumMovie/Completed/daum_train.tsv'
destPath = './Dataset/MergedDataset/Train_NSMC_Daum.tsv'
# reviewHandler.MergeTsvDataset(path_1_tsv, path_2, destPath)

# 2.2   Test - Raw NSMC + daum
path_1_txt = './Dataset/NSMC/RawData/nsmc_test.txt'
path_1_tsv = './Dataset/NSMC/RawData/nsmc_test.tsv'
# reviewHandler.ConvertText2Tsv(path_1_txt, path_1_tsv)

path_2 = './Dataset/DaumMovie/Completed/daum_test.tsv'
destPath = './Dataset/MergedDataset/Test_NSMC_Daum.tsv'
# reviewHandler.MergeTsvDataset(path_1_tsv, path_2, destPath)


'''
    NSMC + Daum + Coupang + Steam
'''
# 3.1   Train - NSMC + Daum + Coupang + Steam
# Re-Processing (Coupang)
path_1_src = './Dataset/Coupang/processed/train_kr.tsv'
path_1_dest = './Dataset/Coupang/processed/RE_train_kr.tsv'
# reviewHandler.ReprocessCoupangReview(path_1_src, path_1_dest)

# 3.2   Test - NSMC + Daum + Coupan + Steam
path_1_src = './Dataset/Coupang/processed/test_kr.tsv'
path_1_dest = './Dataset/Coupang/processed/RE_test_kr.tsv'
# reviewHandler.ReprocessCoupangReview(path_1_src, path_1_dest)