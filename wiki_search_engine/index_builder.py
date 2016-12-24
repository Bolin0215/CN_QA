import jieba

def is_Cn(uchar):
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False

def build_index(file_num, stop_word_set, ttype = 0):
	index = {}
	file_no = 0
	text_path = './corpus/'
	idx_path = './index_v2'
	if ttype == 1:
		text_path = './corpus_sentence/'
		idx_path = './index_sentence'
	while file_no < file_num:
		file_text = open(text_path + str(file_no), 'r')
		text = file_text.read()
		paragraphs = text.split('\n')
		for i in range(len(paragraphs)):
			#seg_list = jieba.cut(paragraphs[i], cut_all=False)
			seg_list = jieba.cut_for_search(paragraphs[i])
			i += 1
			for word in seg_list:
				if len(word) == 1 and is_Cn(word) == False:
					continue
				if word not in stop_word_set:
					# add the record to index
					if word not in index:
						index[word] = {}
						index[word][file_no] = [i]
					else:
						if file_no in index[word]:
							index[word][file_no].append(i)
						else:
							index[word][file_no] = [i]
		file_no += 1
	file_idx = open('idx_path', 'w')
	for i in index:
		record = i + '\t'
		for doc_no in index[i]:
			record += str(doc_no) + ':'
			for paragraph in index[i][doc_no]:
				record += str(paragraph) + ','
			record += '|'
		record += '\n'
		file_idx.write(record)
	file_idx.close()
	return index

def stop_words_set_build():
	file_stop = open('./stopwords.txt', 'r', encoding = "gb2312")
	stop_word_set = file_stop.read().split('\n')
	return stop_word_set

def main():
	stop_word_set = stop_words_set_build()
	build_index(3067, stop_word_set)
	build_index(3067, stop_word_set, 1)

if __name__ == "__main__":
    main()
