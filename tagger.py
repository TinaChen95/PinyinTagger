#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/6 14:54
# @Author  : Ting
import pickle
from collections import Counter


class PinyinTagger:
    def __init__(self, gold_standard, polyphones, k=7):
        assert len({len(value)==len(key) for key, value in gold_standard.items()}) == 1, \
            "some words have multiply pronunciations"

        self.gold_standard = gold_standard
        self.polyphones = polyphones

        self.words = []
        self.k = k

        self.word2id = pickle.load(open('word2id.pkl', 'rb'))
        self.id2word = {str(value): key for key, value in self.word2id.items()}
        all_words_word2vec = {char for word in self.word2id for char in word}
        all_words_gold = {char for word in self.gold_standard for char in word}
        differ = all_words_word2vec - all_words_gold
        if differ != set():
            print('Warning: %d (out of %d) Chinese word are not included in gold standard' %
                  (len(differ), len(all_words_word2vec)))
            print(differ)

        self.words2pinyin = self.tagging_all_words()

    def most_likely_pronunciation(self):
        # seed_word = '干'
        # words = ['干部', '小鱼干', ...]
        with open('nearest.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                seed_word, word, neighbors = line.split(',')
                neighbors = [self.id2word[n] for n in neighbors.split()]
                neighbors = [self.gold_standard[n][n.index(seed_word)]
                             for n in neighbors if n in self.gold_standard[:self.k]]

                if neighbors:
                    counter = Counter(neighbors)
                    self.words2pinyin[word][word.index(seed_word)] = max(counter.keys(), key=lambda x: counter[x])
                else:
                    continue
        return

    def tagging_all_words(self):
        # 读入word2vec词汇表
        self.words2pinyin = {word: ['']*len(word) for word in self.word2id}

        for word in self.words2pinyin:
            if word in self.gold_standard:
                self.words2pinyin[word] = self.gold_standard[word]
            else:
                for i, char in enumerate(word):
                    if char not in self.polyphones and char in self.gold_standard:
                        self.words2pinyin[word][i] = self.gold_standard[char][0]
        self.most_likely_pronunciation()
        return self.words2pinyin


# TODO: fill the file path
gold_standard = pickle.load(open('', 'rb'))
polyphones = pickle.load(open('', 'rb'))

word2pinyin = PinyinTagger(gold_standard, polyphones, k=7)
pickle.dump(word2pinyin.words2pinyin, open('', 'wb'))
