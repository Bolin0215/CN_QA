# CN_QA

### Requirements
+ General
    + Python 3.5.2 & 2.7.9
+ Python Packages
    + Jieba 0.38
    + Keras (theano backend)
    + theano 0.8.2
    + Scikit-learn 0.18.1
    + urllib2 & sgmllib (only python2)

### 问题分类模块
+ 问题分类及预处理
    + 测试问题集放在questions目录下
    + 进入qas_analysis目录
    + python3 utils.py lstm/svm 训练模型并对测试集进行预测并抽取占位词
    + 运行结果为res.txt，保存在questions目录下
    + python3 ensemble.py 使用模板对测试集进行修正
    + 运行结果为final.txt，保存在questions目录下

### 开放测试语料抓取
+ 使用百度知道抓取得到结果
    + 进入online目录
    + python3 search.py 抓取每个页面的前10个结果
    + 运行结果保存在questions/psgs目录下，每200个问题保存为1个文档




