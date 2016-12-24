import os

datadir = '../questions/'
def main():
    ress = []
    for doc in os.listdir(datadir):
        if doc.startswith('res'):
            ress.append(doc)
    contents = []
    length = 0
    for res in ress:
        with open(datadir+res, 'r',encoding="utf-8") as f:
            ret = f.readlines()
            contents.append(ret)
            length = len(ret)
            print(res)
    ans_type = []
    qas = []
    for i in range(length):
        t = []
        qa = ""
        for c in contents:
            qa = c[i].strip().split()[0]
            tmp_type = ""
            if len(c[i].strip().split()) == 3:
                tmp_type = c[i].strip().split()[2]
            elif len(c[i].strip().split()) == 2:
                tmp_type = c[i].strip().split()[1]
            t.append(tmp_type)
        ans_type.append(t)
        qas.append(qa)
    with open('../questions/final.txt','w',encoding="utf-8") as f:
        for i in range(length):
            f.write(qas[i] + ' ' + str(ans_type[i]))
            f.write('\n')

qas_class = {
    'ns': set([u'哪国',u'哪座',u'哪个省',u"哪支球队"]),
    'i': set([u'哪个成语',u'什么成语']),
    'm' : set([u'多少', u'第几', u'哪年',u'哪一年', u'多大',u'哪个数字',u'哪个年代',u"哪个月份"]),
    'nr' : set([u'谁',u'哪位',u'哪一位',u"什么名字"]),
    'nt' : set([u'哪家']),
    't' : set([u'哪个朝代']),
    'nexts': set([u'下一句', u'下句', u'下半句', u'后半句', u'后一句',u"下两句"]),
    'befs': set([u'上一句', u'上句', u'上半句',u'前半句', u'前一句'])
}

def check():
    with open('../questions/res.txt','r', encoding='utf-8') as f:
        ret = f.readlines()
    
    atype = []
    for line in ret:
        line = line.strip()
        content = line.split()[1]
        isget = 0
        if len(line.split()) > 4:
            atype.append(line.split()[-1])
            continue
        for key, value in qas_class.items():
            if isget == 1: break
            for v in value:
                if v in content:
                    atype.append(key)
                    isget = 1
                    break
        
        if isget == 0:
            atype.append(line.split()[-1])
    print (len(ret), len(atype))
    with open('../questions/final.txt', 'w', encoding='utf-8') as f:
        for i in range(len(ret)):
            if len(ret[i].split()) == 3:
                for v in ret[i].split()[:-1]:
                    f.write(v)
                    f.write(' ')
                if '多大' in ret[i]:
                    f.write('多大 ')
                f.write(atype[i] + '\n')
                continue
            for v in ret[i].split()[:-2]:
                f.write(v)
                f.write(' ')
            if '多大' in ret[i]:
                f.write('多大 ')
            else:
                f.write(ret[i].split()[-2] + ' ')
            f.write(atype[i] + '\n')

    
if __name__ == "__main__":
    # main()
    check()
