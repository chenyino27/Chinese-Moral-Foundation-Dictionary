import pandas as pd
import numpy as np
import jieba
import re
import os
from os import path
from datetime import datetime


url = "C:\\Users\\Lenovo\\Desktop\\NLP\\dataset\\fairness_vice"
directory = os.listdir(url)

for f in directory:
    # open each file in directory
    old_url = path.join(url, f)

    # replace wrong . placement
    new_url = old_url.replace(" .", ".")
    os.rename(old_url,new_url)

    print(new_url)
    file = pd.read_csv(new_url)

    # Remove duplicated weibo and preprocessing
    df = file.loc[:, ['content']]
    df.drop_duplicates(inplace=True)
    df['cleaned_content'] = df['content'].str.replace(r'\s*@\S+', '', regex=True)

    # Check whether the weibo after preprocessing still contains keywords
    # 不 means not here, the dataset of 不公平(not fair) contains many words 公平(fair) without 不
    # Thus, we remove 不 here otherwise many useful weibo maybe deleted in this step
    f = f.replace(".csv", "")
    f = f.replace("不","")
    print(f)
    bool = df.cleaned_content.str.contains(f,na=False)
    df = df[bool]

    # Chinese jieba segmentation
    df['jieba_content'] = df['cleaned_content'].apply(lambda x: ' '.join(jieba.lcut(x)))

    # Remove stopwords 
    with open(r"C:\Users\Lenovo\Desktop\NLP\stopwords.txt", "r", encoding='utf-8') as f:
        stopwords = f.readlines()
    stopwords_list = []
    for each in stopwords:
        stopwords_list.append(each.strip('\n'))
    # remove stopwords
    def remove_stopwords(ls):  
        ls = ls.split(" ")
        return [word for word in ls if word not in stopwords_list]

    df['final_data'] = df['jieba_content'].apply(lambda x: remove_stopwords(x))
    print(df.final_data)
    
    


