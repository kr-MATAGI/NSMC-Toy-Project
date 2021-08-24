import urllib.request
import pandas as pd
import os.path

from MyUtils import MakeNSMCDocumentFile, MakeNSMCLabelFile

# url
nsmc_train_url = 'https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt'
nsmc_test_url = 'https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt'

download_path = './Dataset/NSMC/RawData'
nsmc_train_path = download_path + '/nsmc_train.txt'
nsmc_test_path = download_path + '/nsmc_test.txt'

# Download NSMC train, test dataset
print('----Download NSMC Dataset----')
print('Train url: {0}, path: {1}'.format(nsmc_train_url, nsmc_train_path))
print('Test url: {0}, path: {1}'.format(nsmc_test_url, nsmc_test_path))

# Checking
if False == os.path.exists(nsmc_train_path):
    urllib.request.urlretrieve(nsmc_train_url, filename=nsmc_train_path)
else: print('Already Downloaded: ', nsmc_train_path)

if False == os.path.exists(nsmc_test_path):
    urllib.request.urlretrieve(nsmc_test_url, filename=nsmc_test_path)
else: print('Already Downloaded: ', nsmc_test_path)

# Extract 'document'
nsmc_train_table = pd.read_table(nsmc_train_path).dropna()
nsmc_test_table = pd.read_table(nsmc_test_path).dropna()

nsmc_train_doc = nsmc_train_table['document']
nsmc_test_doc = nsmc_test_table['document']
print('\nNSMC Train document size: {}'.format(len(nsmc_train_doc)))
print('NSMC Test document size: {}'.format(len(nsmc_test_doc)))

# Make File which is inclued only 'document'
print('\n----Make NSMC document file----')

nsmc_train_doc_path = './Dataset/NSMC/Splited/before_train_doc_'
nsmc_test_doc_path = './Dataset/NSMC/Splited/before_test_doc_'

MakeNSMCDocumentFile(nsmc_train_doc_path, nsmc_train_doc)
MakeNSMCDocumentFile(nsmc_test_doc_path, nsmc_test_doc)

# Extract 'label'
nsmc_train_label = nsmc_train_table['label']
nsmc_test_label = nsmc_test_table['label']
print('\nNSMC Train label size: {}'.format(len(nsmc_train_label)))
print('NSMC Test label size: {}'.format(len(nsmc_test_label)))

nsmc_train_label_path = './Dataset/NSMC/Splited/train_label.txt'
nsmc_test_label_path = './Dataset/NSMC/Splited/test_label.txt'
MakeNSMCLabelFile(nsmc_train_label_path, nsmc_train_label)
MakeNSMCLabelFile(nsmc_test_label_path, nsmc_test_label)