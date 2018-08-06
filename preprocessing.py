#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/6 15:07
# @Author  : Ting

# use word embedding to calculate the similarity between words

import numpy as np
import pickle
import re
import os


def is_Chinese(word):
    if re.findall('[^\u4e00-\u9fff]', word):
        return False
    return True


def similarity(array1, array2):
    num = array1.dot(array2)
    norm1 = np.linalg.norm(array1, axis=1, keepdims=True)
    norm2 = np.linalg.norm(array2, axis=0, keepdims=True)
    denum = norm1.dot(norm2)
    return num / denum


def remove_non_chinese():
    word2id = dict()
    file = open('word2vec/word2vec', 'w', encoding='utf8')
    with open('word2vec/sgns.merge.bigram', 'r', encoding='utf8') as f:
        line = f.readline()
        total, dim = [int(n) for n in line.strip().split()]
        n = 0
        for i in range(total):
            splits = line.strip().split()
            word = splits[0]
            if len(word) == 1 or not is_Chinese(word):
                continue
            word2id[word] = n
            file.write(line)
            n += 1
    file.close()
    pickle.dump(word2id, open('word2id.pkl', 'wb'))


def calculate_similarity(polyphones, words, file, size_threshold=10000):
    sim_matrix = dict()
    for word in words:
        words = polyphones[word]['words']
        vectors = np.array(polyphones[word]['vectors'])
        if len(vectors) == 0:
            continue
        if len(vectors) > size_threshold:
            print(word + " too much vectors")
            pickle.dump({word: polyphones[word]}, open('extra/%s.pkl' % word, 'wb'))
            continue
        sim_matrix[word] = {'words': words, 'similarity': similarity(vectors, vectors.T)}
    pickle.dump(sim_matrix, open(file, 'wb'))


def read_in_word2vec():
    polyphones = pickle.load(open('polyphones.pkl', 'rb'))
    polyphones = {word: {'words': [], 'vectors': []} for word in polyphones}
    with open('word2vec/word2vec', 'r', encoding='utf8') as f:
        for i, line in enumerate(f.readlines()[1:]):
            splits = line.strip().split()
            word = splits[0]
            vector = [float(s) for s in splits[1:]]
            for char in word:
                if char in polyphones:
                    polyphones[char]['words'].append(word)
                    polyphones[char]['vectors'].append(vector)
            if i % 100000 == 0:
                print(i)
    return polyphones


# remove words that conclude chars that aren't chinese
remove_non_chinese()    # 848281 个 中文词汇

# similarity calculation cannot be done at a time
# we calculate them by small batches
os.mkdir('extra')
polyphones = read_in_word2vec()
n = 0
batch_size = 25
while n < len(polyphones):
    calculate_similarity(polyphones, list(polyphones.keys())[n:n+batch_size],
                         'similarity/%d.pkl' % n)
    n += batch_size
del polyphones

for w in os.listdir('extra'):
    polyphones = pickle.load(open('extra/'+w, 'rb'))
    calculate_similarity(polyphones, polyphones.keys(), 'similarity/'+w)
    os.remove('extra/'+w)
os.removedirs('extra')

# 将排序结果写入文档
word2id = pickle.load(open('word2id.pkl', 'rb'))
with open('nearest.txt', 'w') as f:
    for file in os.listdir('similarity'):
        print(file)
        similarities = pickle.load(open('similarity/'+file, 'rb'))
        for seed_word in similarities:
            words, sim_matrix = similarities[seed_word].values()
            for i, word in enumerate(words):
                nearest = [str(word2id[w]) for w, _ in sorted(zip(words, sim_matrix[i]),
                                                              key=lambda x: x[1], reverse=True)[1:]]
                f.write(seed_word + ',' + word + ',' + ' '.join(nearest) + '\n')
