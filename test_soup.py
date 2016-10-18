import utils
import os
java_path = "C:/Program Files/Java/jdk1.8.0_101/bin/java.exe"
os.environ['JAVAHOME'] = java_path
print(os.environ.get('STANFORD_MODELS'))
from nltk.parse.stanford import StanfordParser
from nltk.tree import ParentedTree
import csv
import sys


def _proccess_string(inp_str):
    inp_str = inp_str.replace('\n', ' ')
    inp_str = inp_str.replace('!', '.')
    inp_str = inp_str.replace('?', '.')
    inp_str = inp_str.replace('\t', '')
    inp_str = inp_str.replace('[', '')
    inp_str = inp_str.replace(']', '')
    inp_str = inp_str.rstrip('\t')
    inp_str = inp_str.replace(';', '.')
    inp_str = inp_str.replace(':', '.')
    return inp_str

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

for root, dirs, files in os.walk(os.path.normpath('C:\\Users\\Marc\\PycharmProjects\\nltk\\texts')):
    for current_file in files:
        path=os.path.join(root, current_file)
        prs_path=os.path.normpath('C:\\Users\\Marc\\PycharmProjects\\nltk\\prses')
        current_file_opened=open(path, encoding='ISO-8859-1')
        prs_file=os.path.join(prs_path, os.path.join(path.split('\\')[-2], path.split('\\')[-1].split('.')[0]+'.prs'))
        try:
            open(prs_file)
        except FileNotFoundError:
            continue
        is_parsed=0
        with open(prs_file, encoding='utf-8') as tsv_inp:
            prs_csv_list = list(csv.reader(tsv_inp, dialect='excel-tab'))
            for line in prs_csv_list:
                if not line[0].startswith('#'):
                    if '_mmbr' in line[13]:
                        is_parsed=1
                        break
            if is_parsed==1:
                continue
        soup=utils.make_soup_with_webpage(current_file_opened, 'html')
        text_src=utils.get_text(soup)
        parser = StanfordParser()

        text_src_unchanged = _proccess_string(text_src)
        text_src=[]
        for l in text_src_unchanged.split('.'):
            if l != "" and len(l.split())<100:
                text_src.append(l + '.')
            else:
                l=l.replace(',','.')
                for e in l.split('.'):
                    if e != "":
                        text_src.append(e + '.')
        text_src.pop()
        print(text_src)
        parsed_text = parser.raw_parse_sents(text_src)

        with open(prs_file, 'w+', encoding='utf-8', newline='') as tsv_out:
            output_prs = csv.writer(tsv_out, dialect='excel-tab')
            word_list=[]
            for lines in parsed_text:
                for sent in lines:
                        ptree = ParentedTree.convert(sent)
                        for sub in ptree.subtrees():
                            if str(sub).count('(') == 1:
                                word_list.append(sub)
            print(word_list)

            for line in prs_csv_list:
                for sub in word_list:
                    lulue=str(sub.leaves()[0])
                    if not line[0].startswith('#'):
                        if str(sub.leaves()[0]) == line[4] and (line[8]=='1' or line[8]=='?'):
                            line[13] += (' '+str(sub.parent()).split('(')[1].replace('\n','').replace(' ','')+'_mmbr')
                            break
                output_prs.writerow(line)

