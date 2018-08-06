# PinyinTagger
A semi-supervised PinyinTagger for Chinese based on Word2Vec+KNN

## 任务简介
目的：基于一个较小的发音词典(gold standard)，为大量中文词汇(82万个)标注发音

中文多音字的发音，是依赖于其本身的词意的。
例如，多音字“好”形容有点多时，读hao3；表示喜爱某个事物时，读hao4。

方法：Word2Vec + KNN
* 预训练Word2vec(82万+词汇），用于计算词汇距离
* 使用KNN，基于邻居投票为候选词进行标注

## 输入输出
* 输入： 较小的发音词典(gold standard)  
* 输出： 82万中文词汇的注音结果

## 研究对象：
* 包括： 词汇中含有多音字，但词汇作为一个整体，只有一个发音。如：美好（mei3 hao3）, 骨干（gu3 gan4）
* 不包括： 作为整体，具有多个读音的词汇。如：提供（ti2 gong1, ti2 gong4）, 好（hao3, hao4）
* 不包括： 命名实体中的多音字

## 模型优缺点：
优点：依据词意，自动标注

缺点：标注结果很依赖 gold standard 的质量

## TODO:
* 调参： KNN的参数K
* 模型效果评估
