# coding: utf-8

# In[1]:

import re
import pandas as pd
import os

work_dir = 'd:/works/project/phone_csf/'
os.chdir(work_dir)

# In[2]:

para_df = pd.read_csv('dataframes/phone_fullframe(title_only).csv', encoding='cp949')
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
        text = para_df['contents'][i]

        if word in para_dict['para_da']:
            text = para.sub(' {}다 '.format(word), text)
            if text != para_df['contents'][i]:
                para_df['contents'][i] = text
            else:
                pass

        elif word in para_dict['para_hada']:
            text = para.sub(' {}하다 '.format(word), text)
            if text != para_df['contents'][i]:
                para_df['contents'][i] = text
            else:
                pass


        elif word in para_dict['to_noun']:
            text = para.sub(' {} '.format(word), text)
            if text != para_df['contents'][i]:
                para_df['contents'][i] = text
            else:
                pass
    print(i, i/len(para_df) * 100, '% completed')

para_df.to_csv('temp_df.csv', index=False, sep='\t')
