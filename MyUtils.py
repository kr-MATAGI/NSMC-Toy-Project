'''
    Make file which is included NSMC's 'docuemnt'
'''
from numpy import NaN


def MakeNSMCDocumentFile(savedPath, docData):
    print('----Start Make Doc File: ', savedPath)

    train_write_size = 10000
    train_total_loop_step = int(len(docData) / train_write_size)

    for idx in range(train_total_loop_step):
        startIdx = idx*train_write_size
        endIdx = idx*train_write_size+train_write_size
        
        write_list = []
        if idx == train_total_loop_step-1: 
            write_list = docData[startIdx:]
        else:
            write_list = docData[startIdx:endIdx]
    
        with open(savedPath+str(idx)+'.txt', mode='w', encoding='utf-8') as f:
            write_count = 0
            for idx, data in enumerate(write_list):
                try:
                    f.write(data + '\n')
                    write_count += 1
                except:
                    print(idx, data)
            print(f'origin: {len(write_list)}, write: {write_count}')


'''
    Make file which is included NSMC's 'label'
'''
def MakeNSMCLabelFile(savedPath, labelData):
    print('----Start Make Label File: ', savedPath)

    with open(savedPath, mode='w', encoding='utf-8') as f:
        write_count = 0
        for idx, data in enumerate(labelData):
            try:
                f.write(str(data) + '\n')
                write_count += 1
            except:
                print(idx)
        print(write_count)