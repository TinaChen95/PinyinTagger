#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 16:01
# @Author  : Ting
import requests
import pickle
import json
import os
mono_url = 'https://hanyu.baidu.com/hanyu/ajax/search_list?wd=%s组词&from=poem&' \
           'userid=962828825&pn=%d&_=1533890304009'
pinyin_url = 'https://hanyu.baidu.com/hanyu/ajax/search_list?py=%s&ptype=zici_tag&' \
             'wd=%s组词&userid=962828825&pn=%d&_=1533886788036'

file = open('fayin.txt', 'a')
word2pinyin = dict()


def get_polyphone_pinyin(char, pinyin):
    page = 1
    while True:
        url = pinyin_url % (pinyin, char, page)
        data = requests.get(url).json()
        if 'ret_array' not in data or not data['ret_array']:
            print(char + 'not collected')
            break
        for word in data['ret_array']:
            file.write(str(word)+'\n')
        update_data(word2pinyin, data['ret_array'])
        if page >= data['extra']['total-page']:
            break
        page += 1


def get_monophone_pinyin(char):
    page = 1
    while True:
        url = mono_url % (char, page)
        data = requests.get(url).json()
        if 'ret_array' not in data or not data['ret_array']:
            print(char + 'not collected')
            break
        for word in data['ret_array']:
            file.write(str(word)+'\n')
        update_data(word2pinyin, data['ret_array'])
        if page >= data['extra']['total-page']:
            break
        page += 1


def update_data(diction, data):
    for d in data:
        word = d['name'][0]
        if word not in diction:
            diction[word] = set()
        diction[word].update(set(d['pinyin']))


char2pinyin = pickle.load(open('all.pkl', 'rb'))
items = list(char2pinyin.items())[:50]
for i, (char, pinyins) in enumerate(items):
    word2pinyin[char] = dict()
    if len(pinyins) > 1:
        for pinyin in pinyins:
            get_polyphone_pinyin(char, pinyin)
    else:
        get_monophone_pinyin(char)
    if i % 100 == 0:
        print(i, items[i: i+100])

# pickle.dump(word2pinyin, open('word2pinyin.pkl', 'wb'))
file.close()


# word2pinyin = dict()
# char2pinyin = pickle.load(open('all.pkl', 'rb'))
# items = list(char2pinyin.items())
# for i, (char, pinyins) in enumerate(items):
#     if len(pinyins) > 1:
#         for pinyin in pinyins:
#             data = pickle.load(open('fayin/%s_%s.pkl' % (char, pinyin), 'rb'))
#             update_data(word2pinyin, data)
#     else:
#         data = pickle.load(open('fayin/%s.pkl' % char, 'rb'))
#         update_data(word2pinyin, data)
# pickle.dump(word2pinyin, open('word2pinyin.pkl', 'wb'))
