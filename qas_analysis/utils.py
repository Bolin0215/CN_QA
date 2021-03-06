#-*-coding:utf-8-*-

import json, math
from sklearn.externals import joblib
import numpy as np
from collections import defaultdict
import jieba
import os    
os.environ['THEANO_FLAGS'] = "device=gpu0"
import theano

class Loader:
    qa_class_path = ""
    @staticmethod
    def load_qa_class():
        with open("../../data/qas_class.json", 'r', encoding='utf-8') as f:
            ret = json.load(f)
        return ret
    
    @staticmethod
    def build_train_test(ratio = None):
        train = {}
        test = {}
        ret = Loader.load_qa_class()
        ratio = ratio or 0.2
        for key, value in ret.items():
            length = len(value)
            train_length = math.ceil(length * (1 - ratio))
            # test_length = length - train_length
            train[key], test[key] = [], []
            for i in range(train_length):
                context = [v.split()[0] for v in value[i].split('|')]
                context = ' '.join(context)
                train[key].append(context)
            for i in range(train_length, length):
                context = [v.split()[0] for v in value[i].split('|')]
                context = ' '.join(context)
                test[key].append(context)
        return train, test

    @staticmethod
    def build_class():
        key2id = {'n': 0, 'i': 1, 'nexts': 7, 'nr': 2, 't': 3, 'nt': 4, 'm': 5, 'ns': 6, 'befs': 8}
        id2key = {0 : 'n', 1: 'i', 7:'nexts', 2 :'nr', 3:'t', 4:'nt', 5:'m', 6:'ns', 8:'befs'}
        return key2id, id2key

    @staticmethod
    def save_model(model, modelpath, option, paramspath = None):
        if option == 'svm':
            joblib.dump(model, modelpath)
        elif option == "lstm":
            json_string = model.to_json()  #等价于 json_string = model.get_config()  
            open(modelpath,'w').write(json_string)    
            model.save_weights(paramspath)
    @staticmethod
    def load_model(modelpath, model, paramspath=None):
        if model == "svm":
            clf = joblib.load(modelpath)
        elif model == "lstm":
            from keras.models import model_from_json
            f = open(modelpath)
            clf = model_from_json(f.read())
            f.close()
            clf.load_weights(paramspath)   
        return clf


    @staticmethod
    def build_vocab():
        ret = Loader.load_qa_class()
        vocab = defaultdict(float)
        max_len = 0
        for key, value in ret.items():
            for v in value:  
                context = [w.split()[0] for w in v.split('|')]
                context = ' '.join(context)
                words = set(context.split())
                if max_len < len(context.split()):
                    max_len = len(context.split())
                for word in words:
                    vocab[word] += 1
        return vocab, max_len

    @staticmethod
    def load_word_vec(vocab):
        word_vecs = {}
        fname = "../../data/w2v-d300.txt"
        with open(fname, "r", encoding="utf-8") as f:
            header = f.readline()
            vocab_size, layer1_size = map(int, header.split())
            # binary_len = np.dtype('float32').itemsize * layer1_size
            # print (vocab_size)
            for line in range(vocab_size):
                word = []
                content = f.readline().strip()
                word = content.split()[0]
                vec = content.split()[1:]
                # if word in vocab:
                word_vecs[word] = np.array(vec, dtype='float32')  
        return word_vecs

    @staticmethod
    def get_W(word_vecs, k=300):
        """
        Get word matrix. W[i] is the vector for word indexed by i
        """
        vocab_size = len(word_vecs)
        word_idx_map = dict()
        W = np.zeros(shape=(vocab_size+1, k), dtype='float32')
        i = 1
        for word in word_vecs:
            W[i] = word_vecs[word]
            word_idx_map[word] = i
            i += 1
        return W, word_idx_map
    
    @staticmethod
    def add_unknown_words(word_vecs, vocab, min_df=1, k=300):
        """
        For words that occur in at least min_df documents, create a separate word vector.    
        0.25 is chosen so the unknown vectors have (approximately) same variance as pre-trained ones
        """
        for word in vocab:
            if word not in word_vecs and vocab[word] >= min_df:
                word_vecs[word] = np.random.uniform(-0.25,0.25,k) 

what_word = set(['什么','哪一位','谁','多少','哪座','第几','何时','是？','为？',\
                '哪位', '哪个', '哪','多'])
what_class = { '哪国' : 'ns',\
               '哪位':'nr',\
                }

def extract_word(q):
    if q[-1] == u"是" or q[-1] == u"为":
        return '?'
    seg_list = jieba.lcut(q)
    

    for i in range(len(seg_list)):
        for word in what_word:
            if seg_list[i] == word:
                return word

    for seg in seg_list:
        for word in what_word:
            if seg.find(word, 0, len(word)) > -1:
                return seg
    return None

def main(model):
    qa = None
    if model == 'lstm':
        import lstm
        qa = lstm.LSTM()
    else:
        import svm
        qa = svm.SVM()
    if qa == None:
        qa = svm.SVM()
    qa.train_save()
    
def forward(qa):
    with open('../questions/questions.txt','r') as f:
        contents = f.readlines()

    res, keys = [], []
    for sent in contents:
        sent = sent.strip().split()[1]
        res.append(qa.forward(sent))
        keys.append(extract_word(sent))
    with open('../questions/res.txt','w') as f:
        for i in range(len(contents)):
            f.write(contents[i].strip())
            if keys[i]:
                f.write(' ' + keys[i])
            if keys[i] in what_class.keys():
                f.write(' ' + what_class[keys[i]])
            else:
                f.write(' ' + res[i])
            f.write('\n')
    

if __name__ == "__main__":

    import sys
    if len(sys.argv) != 2:
        print ('Error')
        sys.exit(0)
        
    main(sys.argv[1])
    pass

