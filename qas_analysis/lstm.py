from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Merge
from keras.layers.embeddings import Embedding
from keras.layers import recurrent, TimeDistributed
from keras.layers import convolutional, pooling
import keras
import numpy as np
import jieba
import utils
from utils import Loader

class LSTM(object):
    def __init__(self, load = None):
        self.model_path = "../../data/lstm_model.json"
        self.params_path = "../../data/lstm_params.h5"
        
        self.vocab, self.max_len = Loader.build_vocab()
        print ("data loaded!")
        print ("vocab size: " + str(len(self.vocab)))
        print ("max sentence length: " + str(self.max_len))
        self.w2v = Loader.load_word_vec(self.vocab)
        print ("word2vec loaded!")
        print ("num words already in word2vec: " + str(len(self.w2v)))
        Loader.add_unknown_words(self.w2v, self.vocab)
        self.W, self.word_idx_map = Loader.get_W(self.w2v)
        self.c2id, self.id2c = Loader.build_class()
        print (self.c2id)
        if load:
            self.model = Loader.load_model(self.model_path, "lstm", self.params_path)
            return
        self.model = Sequential()
        self.model.add(Embedding(len(self.word_idx_map)+1, 300, weights = [self.W]))
        self.model.add(recurrent.LSTM(output_dim=100, activation='tanh', dropout_W=0, dropout_U=0))
        #self.model.add(convolutional.Convolution1D(100, 3, activation='tanh', border_mode='same'))
        self.model.add(pooling.GlobalMaxPooling1D())
        #self.model.add(Dropout(0.2))
        self.model.add(Dense(7))
        self.model.add(Activation('softmax'))
        print (self.model.summary())
        
        

        rmsprop = keras.optimizers.rmsprop(lr=0.002)
        self.model.compile(loss='categorical_crossentropy', optimizer=rmsprop, metrics=["accuracy"])
        #self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics = ['categorical_accuracy'])
            
    def train_save(self):
        train_data, train_target, test_data, test_target = self.get_train_test_data()
        print (len(train_data), len(train_target))
        print (len(test_data), len(test_target))
        train_data = np.array(train_data)
        test_data = np.array(test_data)
        print (len(train_data))
        best = -999999
        for i in range(10):
            self.model.fit(train_data, train_target, batch_size=20, nb_epoch=1, shuffle = True)
            score = self.model.evaluate(test_data, test_target, batch_size=20)
            print (score)
            if score[1] > best:
                print ('forward!!')
                utils.forward(self)
                best = score[1]
                Loader.save_model(self.model, self.model_path, "lstm", self.params_path)

        
    
    def forward(self, sent):
        if '下一句' in sent or '下句' in sent:
            return 'nexts'
        if '上一句' in sent or '上句' in sent:
            return 'befs'

        sent = jieba.lcut(sent)
        ids = []
        for i in range(self.max_len):
            if i < len(sent):
                ids.append(self.word_idx_map.get(sent[i],0))
            else:
                ids.append(0)
        test = np.array([ids])
        predict = self.model.predict(test, batch_size = 1)
        return self.id2c[np.argmax(predict[0])]

    def get_train_test_data(self):
        train_data, test_data = [], []
        train_target, test_target = [], []
        train_dict, test_dict = Loader.build_train_test()
        for key, value in train_dict.items():
            for v in value:
                ids = []
                length = self.max_len
                for i in range(length):
                    if i < len(v.split()):
                        ids.append(self.word_idx_map[v.split()[i]])
                    else:
                        ids.append(0)
                train_data.append(ids)
                target = [0,0,0,0,0,0,0]
                target[self.c2id[key]] = 1
                train_target.append(target)

        for key, value in test_dict.items():
            for v in value:
                ids = []
                length = self.max_len
                for i in range(length):
                    if i < len(v.split()):
                        ids.append(self.word_idx_map[v.split()[i]])
                    else:
                        ids.append(0)
                test_data.append(ids)
                target = [0,0,0,0,0,0,0]
                target[self.c2id[key]] = 1
                test_target.append(target)

        return train_data, train_target, test_data, test_target

    
