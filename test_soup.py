import utils
import os
java_path = "C:/Program Files/Java/jdk1.8.0_101/bin/java.exe"
os.environ['JAVAHOME'] = java_path
print(os.environ.get('STANFORD_MODELS'))
from nltk.parse.stanford import StanfordParser
from nltk.tree import ParentedTree
import csv
import sys

maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True

for d, dirs, files in os.walk(os.path.normpath('C:\\Users\\Marc\\PycharmProjects\\nltk\\texts')):
    for fe in files:
        path=os.path.join(d,fe)
        prs_path=os.path.normpath('C:\\Users\\Marc\\PycharmProjects\\nltk\\prses')
        f=open(path,encoding='ISO-8859-1')
        prs_file=os.path.join(prs_path, os.path.join(path.split('\\')[-2], path.split('\\')[-1].split('.')[0]+'.prs'))
        try:
            open(prs_file)
        except FileNotFoundError:
            continue
        flag1=0
        with open(prs_file, encoding='utf-8') as tsv_inp:
            lulcsv = list(csv.reader(tsv_inp, dialect='excel-tab'))
            for line in lulcsv:
                if not line[0].startswith('#'):
                    if '_mmbr' in line[13]:
                        flag1=1
                        break
            if flag1==1:
                continue
        soup=utils.make_soup_with_webpage(f,'html')
        lul=utils.get_text(soup)
        parser = StanfordParser()
        lul = lul.replace('\n', ' ')
        lul = lul.replace('!','.')
        lul = lul.replace('?','.')
        lul = lul.replace('\t','')
        lul = lul.replace('[','')
        lul = lul.replace(']', '')
        lul=lul.rstrip('\t')
        lul = lul.replace(';','.')
        lul=lul.replace(':','.')
        lu = lul
        lul=[]
        for l in lu.split('.'):
            if l != "" and len(l.split())<100:
                lul.append(l+'.')
            else:
                l=l.replace(',','.')
                for e in l.split('.'):
                    if e != "":
                        lul.append(e+'.')
        lul.pop()
        print(lul)
        sents = parser.raw_parse_sents(lul)

        with open(prs_file, 'w+', encoding='utf-8', newline='') as tsv_out:
            ulucsv = csv.writer(tsv_out, dialect='excel-tab')
            word_list=[]
            for lines in sents:
                for sent in lines:
                        ptree = ParentedTree.convert(sent)
                        for sub in ptree.subtrees():
                            flag=True
                            if str(sub).count('(') == 1:
                                word_list.append(sub)
            print(word_list)

            for line in lulcsv:
                for sub in word_list:
                    lulue=str(sub.leaves()[0])
                    if not line[0].startswith('#'):
                        if str(sub.leaves()[0]) == line[4] and (line[8]=='1' or line[8]=='?'):
                            line[13] += (' '+str(sub.parent()).split('(')[1].replace('\n','').replace(' ','')+'_mmbr')
                            break
                ulucsv.writerow(line)

