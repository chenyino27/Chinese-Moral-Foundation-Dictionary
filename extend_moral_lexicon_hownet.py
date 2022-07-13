import OpenHowNet
import os
import csv

'''
HowNet Manual: https://gitee.com/thunlp/OpenHowNet (cn) https://github.com/thunlp/OpenHowNet (en)
'''

def get_csv(dir_path):
    list_csv = []
    dir_list = os.listdir(dir_path)
    for cur_file in dir_list:
        path = os.path.join(dir_path,cur_file)
        if os.path.splitext(path)[1] == '.csv':
            cur_path=os.path.splitext(path)[0]
            list_csv.append(cur_path.split('/')[1])
    return list_csv

#Find the corresponding 5 synonyms for 1 initial word through HOWNET, to expand the initial MFD
def lexicon_expand_HowNet(csv_file):
    # OpenHowNet.download()#Using Hownet for the first time needs to download Yiyuan data
    hownet = OpenHowNet.HowNetDict()
    hownet_dict_advanced = OpenHowNet.HowNetDict(use_sim=True)

    #read initial lexicon
    file='five_dimension/'+csv_file+'.csv'

    keywords=[]

    with open(file,'r',encoding='utf-8-sig') as f:
        lines=f.readlines()
        for line in lines:
            words=line.replace('\n','').split(',')
            keywords.append(words[1])

    synonymous=[]

    #search synonymous of each word in HowNet
    for keyword in keywords:
        synonymous.append(keyword)
        length=len(synonymous)
        query_result = hownet_dict_advanced.get_nearest_words_via_sememes(keyword,15)
        if query_result:#if this word is in HowNet, find three non-repeated words that are closest to it
            example=query_result[0]
            for word in example["synset"]:
                if word['word'] in synonymous:
                    continue
                else:
                    synonymous.append(word['word'])
                if len(synonymous)-length==6:
                    print(synonymous)
                    break
        else:
            print(synonymous)
    write_to_csv(csv_file,synonymous)

#write all words into .csv files
def write_to_csv(csv_file,synonymous):
    result_file='five_dimension_HowNet/'+csv_file+'.csv'
    with open((result_file), 'a', encoding='utf-8-sig', newline='') as (f):
        writer = csv.writer(f)
        for word in synonymous:
            writer.writerow([word])


def main():
    dir_path = r'five_dimension'
    list_csv=get_csv(dir_path)
    for csv_file in list_csv:
        lexicon_expand_HowNet(csv_file)


if __name__ == '__main__':
    main()