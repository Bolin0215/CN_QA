def file_make(ttype = 0):
	fileraw = open('./wiki_chs', 'r')
	text = fileraw.read()
	fileraw.close()
	docs = text.split('</doc>\n')
	doc_num = len(docs)
	print(docs[-1])	
	st = 0
	count = 0
	path = './corpus/'
	if ttype == 1:
		path = './corpus_sentence/'
	while st < doc_num:
		text = ''
		length = 0
		while length < 136000 and st < doc_num:
			text += docs[st]
			length += len(docs[st])
			st += 1
		#print(length)
		if ttype == 1:
			text = text.replace('。', '。\n')
		paragraphs = text.split('\n')
		text = ''
		for p in paragraphs:
			if len(p) == 0:
				continue
			text += p + '\n'
		filenow = open(path + str(count), 'w')
		filenow.write(text)
		filenow.close()
		count += 1

def main():
    file_make()
    file_make(1)

if __name__ == "__main__":
    main()