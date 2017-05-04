# -*- coding: utf-8 -*-

import re

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

def paraph(df, i):
    for word in para_lst:
        para = re.compile(r'{}\w*'.format(word))

        if word in para_dict['para_da']:
            df['contents'][i] = para.sub(' {}다 '.format(word), df['contents'][i])
    
        elif word in para_dict['para_hada']:
            df['contents'][i] = para.sub(' {}하다 '.format(word), df['contents'][i])
    
        elif word in para_dict['to_noun']:
            df['contents'][i] = para.sub(' {} '.format(word), df['contents'][i])
        
    return df['contents'][i]