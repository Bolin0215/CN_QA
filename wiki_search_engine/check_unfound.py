def find_unfound(type = 0):
	path = './candidates.para2sent.all'
	if type == 1:
		path = './candidates.sent'
	file_result = open(path, 'r')
	data = file_result.read().split('</question>\n')[0:-1]
	lost = -1
	qno = []
	for i in data:
		ed = i.find('>')
		no = int(i[13:ed])
		i = i.split('\n')
		if len(i) < 3:
			print (no)
			qno.append(no)
			lost += 1
	print ('Lost = ' + str(lost))
	return qno

def gen_question_round2(qno, rno):
	qfile = open('./questions.txt', 'r')
	data = qfile.read().split('\n')
	qfile.close()
	q2file = open('./questions.r' + str(rno) + '.txt', 'w') 
	for q in qno:
		q2file.write(data[q-1] + '\n')
	q2file.close()

def merge(file1, file2):
	data = file1.read().split('</question>\n')[0:-1]
	data.extend(file2.read().split('</question>\n')[0:-1])
	length = len(data)
	all_record = ['']*length
	for i in data:
		ed = i.find('>')
		no = int(i[13:ed])
		all_record[no] = i + '</question>\n'
	file_t = open('./candidates.para2sent.all', 'w')
	for i in range(length):
		file_t.write(all_record[i])


def main():
	gen_question_round2(find_unfound(), 3)
	# file1 = open('./candidates.para2sent', 'r')
	# file2 = open('./candidates.para2sent.round2', 'r')
	# merge(file1, file2)
	# file1.close()
	# file2.close()

if __name__ == "__main__":
    main()
