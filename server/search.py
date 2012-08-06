#encoding=utf-8

from smallseg.smallseg import SEG
import os
import json

seg = SEG()
WIKI_PATH = os.path.abspath(os.path.dirname(__name__)) + '/wiki/'
def cuttest(text):
    wlist = seg.cut(text)
    wlist.reverse()
    tmp = " | ".join(wlist)
    print tmp
    print "================================"

def get_data_files():
	for parent, dirname, filenames in os.walk(WIKI_PATH):
		for filename in filenames:
			if filename == 'data.json':
				yield os.path.join(parent, filename)


index = {}

def extract_sentence(content, word):
	c = content.find(word)
	s = 0
	if c - 10 > 0: s = c - 10
	e = len(content)
	if c + 10 <= len(content) : e = c + 10
	return content[s:e]


def add_to_index(content, page_name):
 	wlist = seg.cut((page_name+content).encode('utf-8'))
	for w in wlist:
		t = index.get(w, [])
		t.append({'page': page_name, 'content': extract_sentence(content, w)})
		index[w.lower()] = t

for filename in get_data_files():
	c = []
	with open(filename, 'r') as fp:
		c = json.loads(fp.read())
	c = c[-1]
	page_name = filename.split(WIKI_PATH)[1].replace('/data.json','')
	add_to_index(c['content'], page_name)

 
