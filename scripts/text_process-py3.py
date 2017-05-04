# coding: utf-8

# In[1]:

import re
import csv
import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer

work_dir = 'd:/document/project/phone_csf'
os.chdir(work_dir)


# ### text feature extraction example

# In[191]:

ex_vectorizer = CountVectorizer(min_df=1)
ex_corpus = np.array(['This is the first document.',
          'This is the second second document.',
          'And the third one.',
          'Is this the first document?'])
ex_X = ex_vectorizer.fit_transform(ex_corpus)
ex_X


# In[192]:

ex_vectorizer.get_feature_names()


# In[193]:

ex_X.toarray().sum(axis=0)


# ### apply

# In[194]:

raw_text = pd.read_csv('./dataframes/after_paraphrasing.csv', encoding='cp949')
corpus = np.array(raw_text['V1'])
print(len(corpus))
print(corpus[0:3])


# In[238]:

vectorizer = CountVectorizer(min_df = 0.001, token_pattern=r'\w+')
X = vectorizer.fit(corpus)
X_t = vectorizer.fit_transform(corpus)
X_t


# In[239]:

print(len(X.vocabulary_))
print(len(vectorizer.get_feature_names()))
vectorizer.get_feature_names()


# In[240]:

word_sum = X_t.toarray().sum(axis=0)
word_name = vectorizer.get_feature_names()
word_dict = {}

for i in range(len(word_sum)):
    word_dict[word_name[i]] = word_sum[i]


# In[241]:

print(vectorizer.get_feature_names()[150:160])
print(word_sum[150:160])


# In[242]:

word_dict


# In[243]:

with open('csf_freq(after_para).csv', 'w') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, word_dict.keys(), delimiter=',', lineterminator='\n')
    w.writeheader()
    w.writerow(word_dict)


# In[2]:

para_df = pd.read_csv('dataframes/pcsf_dataframe(ap).csv', encoding='cp949')
para_df.tail()


# ### paraphrasing

# In[3]:

da = ['좋', '힘들', '어둡', '잘되',  '나쁘', '거슬리', '즐겁', '안타깝',
        '부럽', '안되', '빠르', '부드럽', '괜찮', '심하', '잘하', '편하',
        '귀찮', '무겁', '어렵', '느리', '끌리', '오래가', '뜨겁', '비싸',
        '예쁘', '신경쓰', '새롭', '늦', '이쁘', '싫', '아쉽', '가볍']
hada = ['욕', '잘못', '망', '무난']
noun = ['고장', '짜증']

para_dict = {'para_da': da, 'para_hada': hada, 'to_noun': noun}

def paralst_create(*args):
    para_lst = []
    for lst in args:
        for i in lst:
            para_lst.append(i)
    return para_lst

para_lst = paralst_create(da, hada, noun)


# In[ ]:

for i in range(0, len(para_df)):
    for word in para_lst:
        para = re.compile(r'{}\w*'.format(word))

        if word in para_dict['para_da']:
            para_df['contents'][i] = para.sub(' {}다 '.format(word), para_df['contents'][i])

        elif word in para_dict['para_hada']:
            para_df['contents'][i] = para.sub(' {}하다 '.format(word), para_df['contents'][i])

        elif word in para_dict['to_noun']:
            para_df['contents'][i] = para.sub(' {} '.format(word), para_df['contents'][i])
    print(i/len(para_df) * 100, '% completed')
        
# In[79]:

after_para.tail()


# In[80]:

after_para.to_csv('after_paraphrasing.csv', index=False, sep='\t')

