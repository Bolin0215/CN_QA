import jieba
import index_builder

class wiki_searcher():
	word2text = {}
	#word2freq = {}
	stop_word_set = []
	filepath = ''
	def __init__(self, text_arch):
		self.stop_word_set = index_builder.stop_words_set_build()
		index_path = ''
		# text devided by paragraph
		if text_arch == 0:
			index_path = './index_v2'
			self.filepath = './corpus/'
		# text devided by sentence
		if text_arch == 1:
			index_path = './index_sentence'
			self.filepath = './corpus_sentence/'
		index_file = open(index_path, 'r')
		index_data = index_file.read()
		index_file.close()
		records = index_data.split('\n')[0:-1]
		# format of record: [word]\t[file_no:line1,line2,^,linek,|]
		# build dictionary
		for r in records:
			r = r.split('\t')
			self.word2text[r[0]] = {}
			file_and_line = r[1].split('|')[0:-1]
			# freq = 0
			for f in file_and_line:
				f, f_line_list = f.split(':')
				f_lines = f_line_list.split(',')[0:-1]
				self.word2text[r[0]][int(f)] = []
				for l in f_lines:
					self.word2text[r[0]][int(f)].append(l)
			# 	freq += len(set(self.word2text[r[0]][int(f)]))
			# self.word2freq[r[0]] = freq

	def search_by_word_print(self, word):
		if word not in self.word2text:
			print('NO RESULT FOUND')
			return []
		file_and_line = self.word2text[word]
		all_text = []
		for i in file_and_line:
			print ('File: ' + str(i))
			file4text = open(self.filepath + str(i), 'r')
			texts = file4text.read().split('\n')
			file4text.close()
			for l in file_and_line[i]:
				all_text.append(texts[int(l)-1])
				print('	Line: ' + str(l))
				print(all_text[-1])
		return all_text

	def search_by_word(self, word):
		if word not in self.word2text:
			print('NO RESULT FOUND')
			return []
		file_and_line = self.word2text[word]
		all_text = []
		for i in file_and_line:
			file4text = open(self.filepath + str(i), 'r')
			texts = file4text.read().split('\n')
			file4text.close()
			for l in file_and_line[i]:
				all_text.append(texts[int(l)-1])
		return all_text

	def search_by_words_and(self, wordlist):
		all_text = []
		file_pos_set = []
		for w in wordlist:
			if w not in self.word2text:
				#return []
				continue
			cur_file_pos = self.word2text[w].keys()
			file_pos_set.append(cur_file_pos)
		if len(file_pos_set) < 1:
			return []
		file_pos = file_pos_set[0]
		for flist in file_pos_set:
			file_pos = [file_no for file_no in flist if file_no in file_pos]
		if len(file_pos) == 0:
			return []
		line_pos = []
		for file_no in file_pos:
			line_pos_set = []
			for word in wordlist:
				if word not in self.word2text:
					continue
				line_pos_set.append(self.word2text[word][file_no])
			tmp_line_pos = line_pos_set[0]
			for plist in line_pos_set:
				tmp_line_pos = [line_no for line_no in plist if line_no in tmp_line_pos]
			pos = []
			for i in tmp_line_pos:
				pos.append((file_no, i))
			line_pos.extend(pos)
		all_text = []
		# print for debugging
		for i in line_pos:
			#print ('File: ' + str(i[0]))
			file4text = open(self.filepath + str(i[0]), 'r')
			texts = file4text.read().split('\n')
			file4text.close()
			#print('	Line: ' + i[1])
			all_text.append(texts[int(i[1])-1])
			#print(all_text[-1])
		# print end
		return all_text

	# def parser_old(self, sent):
	# 	from pyltp import Segmentor
	# 	segmentor = Segmentor()  # 初始化实例
	# 	segmentor.load('./ltp_data/cws.model')  # 加载模型
	# 	words = segmentor.segment(sent)  # 分词
	# 	segmentor.release() 
	# 	from pyltp import Postagger
	# 	postagger = Postagger() # 初始化实例
	# 	postagger.load('./ltp_data/pos.model')  # 加载模型
	# 	postags = postagger.postag(words)  # 词性标注
	# 	postagger.release() 
	# 	ret_word = []
	# 	# get nouns
	# 	for i in range(len(words)):
	# 		if postags[i] == 'n':
	# 			if (i > 1 and ('哪' in words[i-1] or words[i-1] == '什么')) or (i > 2 and words[i-2] == '哪'):
	# 				continue
	# 			#print(words[i])
	# 			ret_word.append(words[i])
	# 	from pyltp import NamedEntityRecognizer
	# 	recognizer = NamedEntityRecognizer() # 初始化实例
	# 	recognizer.load('./ltp_data/ner.model')  # 加载模型
	# 	netags = recognizer.recognize(words, postags)  # 命名实体识别
	# 	recognizer.release()
	# 	# get names
	# 	for i in range(len(words)):
	# 		if netags[i] != 'O':
	# 			#print(words[i])
	# 			ret_word.append(words[i])
	# 	ret_word = list(set(ret_word))
	# 	#print (ret_word)
	# 	return ret_word

	def parser(self, sent):
		import jieba.posseg as pseg
		words = pseg.cut(sent)
		ret_word = []
		ret_word_eu = []
		ret_word_min = []
		former = ''
		for word, flag in words:
			#print('%s %s' % (word, flag))
			if flag[0] == 'n':
				ret_word.append(word)
				if '哪' in former or former == '什么':
					continue
				ret_word_eu.append(word)
				if 'nr' in flag or flag == 'ns':
					ret_word_min.append(word)
			if flag[0] == 'm':
				ret_word.append(word)
				ret_word_eu.append(word)
			former = word
		ret_word = list(set([word for word in ret_word if word not in self.stop_word_set]))
		ret_word_eu = list(set([word for word in ret_word_eu if word not in self.stop_word_set]))
		ret_word_min = list(set([word for word in ret_word_min if word not in self.stop_word_set]))
		return ret_word, ret_word_eu, ret_word_min

	# def search_by_NE(self, query):
	# 	word_set = self.parser(query)
	# 	word_set = [word for word in word_set if word not in self.stop_word_set]
	# 	return self.search_by_words_and(word_set)
		
	def punc_filter(self, wordlist):
		ret_list = []
		for word in wordlist:
			if len(word) > 1:
				ret_list.append(word)
			else:
				if index_builder.is_Cn(word):
					ret_list.append(word)
		return ret_list

	# def VSM(self, query, sentence):
	# 	wordlist_q = jieba.cut(query, cut_all=False)
	# 	wordlist_q = [word for word in wordlist_q if (word not in self.stop_word_set and word in self.word2freq)]
	# 	wordlist_q = self.punc_filter(wordlist_q)
	# 	wordlist_s = jieba.cut(sentence, cut_all=False)
	# 	wordlist_s = [word for word in wordlist_s if (word not in self.stop_word_set and word in self.word2freq)]
	# 	wordlist_s = self.punc_filter(wordlist_s)
	# 	wordlist = wordlist_s
	# 	wordlist.extend(wordlist_q)
	# 	wordlist = list(set(wordlist))
	# 	up = 0.0
	# 	for w in wordlist:
	# 		up += query.count(w) * sentence.count(w) * self.word2freq[w] * self.word2freq[w]
	# 	d1 = 0.0
	# 	for w in wordlist_s:
	# 		d1 += sentence.count(w) * self.word2freq[w] * sentence.count(w) * self.word2freq[w]
	# 	d2 = 0.0
	# 	for w in wordlist_q:
	# 		d2 += query.count(w) * self.word2freq[w] * query.count(w) * self.word2freq[w]
	# 	down = (d1 * d2) ** 0.5
	# 	return up / down

	def score_naive(self, query, sentence):
		length = len(sentence)
		if length < 6:
			return 0.0
		import jieba.posseg as pseg
		qwords = pseg.cut(query)
		score = 0.0
		# bonus for quota
		if '“' in query:
			count = query.count('“')
			cur = 0
			for i in range(count):
				st = query.find('“', cur) + 1
				ed = query.find('”', cur)
				quota = query[st:ed]
				#print(quota)
				if quota in sentence:
					#print('BONUS for ' + quota)
					score += 500
					if len(quota) >= 6:
						score += 500
				cur = st
		if '《' in query:
			count = query.count('《')
			cur = 0
			for i in range(count):
				st = query.find('《', cur) + 1
				ed = query.find('》', cur)
				quota = query[st:ed]
				#print(quota)
				if quota in sentence:
					#print('BONUS for ' + quota)
					score += 500
				cur = st
		# bonus end
		seen = []
		for word, flag in qwords:
			if word in self. stop_word_set or word in seen :
				continue
			seen.append(word)
			if word not in sentence:
				continue
			if flag[0] == 'a' or flag[0] == 'v' or flag[0] == 'n':
				score += 100 + sentence.count(word)
				if flag[0:2] == 'nr' or flag[0:2] == 'ns' or flag[0:2] == 'nt' or flag[0:2] == 'nz':
					score += 50
			if flag == 'm':
				if len(word) > 1:
					score += 100
				else:
					if word in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
						pos = sentence.find(word)
						if (pos > 1 and sentence[pos-1] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) and (pos+1 < length and sentence[pos+1] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
							score += 100
		#print(seen)
		#score = score / (length ** 0.5) 
		#!!! decide whether use sqrt in out layer
		return score

	def search_top_k(self, query, k, ttype = 1):
		wordlist = jieba.cut(query, cut_all=False)
		wordlist = [word for word in wordlist if word not in self.stop_word_set]
		wordlist = self.punc_filter(wordlist)
		all_text = self.search_by_words_and(wordlist)
		all_text = list(set(all_text))
		# if len(all_text) < k:
		# 	# get more text with logic OR and then rank the text
		# 	wlist, wlist_eu, wlist_min = self.parser(query)
		# 	all_text = self.search_by_words_and(wlist)
		# 	all_text = list(set(all_text))
		# 	if len(all_text) < k:
		# 		all_text = self.search_by_words_and(wlist_eu)
		# 		all_text = list(set(all_text))
		# 		if len(all_text) < k and len(wlist_min) > 0:
		# 			all_text = self.search_by_words_and(wlist_min)
		# 			all_text = list(set(all_text))
		if len(all_text) < k:
			# get more text with logic OR and then rank the text
			wlist, wlist_eu, wlist_min = self.parser(query)
			all_text = self.search_by_words_and(wlist)
			all_text = list(set(all_text))
			if len(all_text) < k:
				all_text = self.search_by_words_and(wlist_eu)
				all_text = list(set(all_text))
				if len(all_text) < k:
					if len(wlist_min) > 0:
						all_text = self.search_by_words_and(wlist_min)
						all_text = list(set(all_text))
					# no result even searching by min set
					else:
						if len(all_text) == 0 and len(wlist_eu) > 0:
							for i in wlist_eu:
								# the boundary is set due to the freq of several most common words
								if (i not in self.word2freq) or (self.word2freq[i] > 90000):
									continue
								all_text.extend(self.search_by_word(i))
		if len(all_text) <= k:
			return all_text
		# then rank and return the top k
		score_sent = []
		for sentence in all_text:
			score = self.score_naive(query, sentence)
			if ttype == 1:
				score = score / (len(sentence) ** 0.5)
			score_sent.append((score, sentence))
		score_sent = sorted(score_sent, key = lambda t:-t[0])
		ret_text = []
		for r in score_sent[0:k]:
			#print (r[0]) # print the score
			ret_text.append(r[1])
		return ret_text

def punc_filter(wordlist):
	ret_list = []
	for word in wordlist:
		if len(word) > 1:
			ret_list.append(word)
		else:
			if index_builder.is_Cn(word):
				ret_list.append(word)
	return ret_list

def test_1():
	devide_by = int(input('Select min unit to devide the text: 1. paragraph; 2. sentence\n'))
	if devide_by == 1:
		searcher = wiki_searcher(0)
	if devide_by == 2:
		searcher = wiki_searcher(1)
	if devide_by != 1 and devide_by != 2:
		print('WRONG INPUT!')
		exit()
	mode = input('Select a mode: 1. search by word; 2. search by a group of words; 3. search by sentence\n')
	if mode == '1':
		while True:
			word = input('Input the word you want to search:\n')
			searcher.search_by_word_print(word)
	if mode == '2':
		while True:
			wordlist = input('Input words devided by space:\n')
			wordlist = wordlist.split(' ')
			searcher.search_by_words_and(wordlist)
	if mode == '3':
		while True:
			sentence = input('Input the sentence:\n')
			wordlist = jieba.cut(sentence, cut_all=False)
			#stop_word_set = index_builder.stop_words_set_build()
			wordlist = [word for word in wordlist if word not in searcher.stop_word_set]
			wordlist = punc_filter(wordlist)
			print(wordlist)
			searcher.search_by_words_and(wordlist)
	print('WRONG MODE! PLEASE INPUT 1, 2, or 3 TO MAKE CHOICE.')
	exit()

# def test_2():
# 	searcher = wiki_searcher(1)
# 	while True:
# 		word = input('Input the word:\n')
# 		print('FREQ(' + word + ') = ' + str(searcher.word2freq[word]))

def test_3():
	searcher = wiki_searcher(1)
	while True:
		query = input('Input the query:\n')
		text = searcher.search_top_k(query, 10)
		count = 1
		for s in text:
			print(str(count) +': ')
			print(s)
			count += 1

def get_condidates_by_sentences_search():
	searcher = wiki_searcher(1)
	file_query = open('./questions.txt', 'r')
	qs = file_query.read().split('\n')
	file_query.close()
	for q in qs:
		file_sent = open('./candidates.sent', 'a')
		q_no, query = q.split('\t')
		file_sent.write('<question id=' + str(q_no) + '>\n')
		text = searcher.search_top_k(query, 10)
		for s in text:
			file_sent.write('答：' + s + '\n')
		file_sent.write('</question>\n')
		file_sent.close()
	#print ('Finish successfully!')

def get_condidates_by_para_search():
	searcher = wiki_searcher(0)
	file_query = open('./questions.txt', 'r')
	qs = file_query.read().split('\n')
	file_query.close()
	for q in qs:
		file_sent = open('./candidates.para2sent', 'a')
		q_no, query = q.split('\t')
		text = searcher.search_top_k(query, 10, 0)
		sent_set = []
		for s in text:
			s = s.replace('。', '。\n')
			s = s.split('\n')
			sent_set.extend(s)
		sent_set = list(set(sent_set))
		score_sent = []
		for sentence in sent_set:
			if len(sentence) == 0:
				continue
			score = searcher.score_naive(query, sentence) / (len(sentence) ** 0.5)
			score_sent.append((score, sentence))
		score_sent = sorted(score_sent, key = lambda t:-t[0])
		ret_text = []
		bound = min(len(score_sent), 10)
		for r in score_sent[0:bound]:
			#print (r[0]) # print the score
			ret_text.append(r[1])
		file_sent.write('<question id=' + str(q_no) + '>\n')
		for s in ret_text:
			file_sent.write('答：' + s + '\n')
		file_sent.write('</question>\n')
		file_sent.close()
	print ('Finish successfully!')

def main():
	get_condidates_by_para_search()

if __name__ == "__main__":
	main()