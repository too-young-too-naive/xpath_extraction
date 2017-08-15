import os
import json
import io
import re
import codecs
from collections import OrderedDict
from scrapy import Selector



def generate_map(directory, dic):
    for (cur, dirs, files) in os.walk(directory):
	for fp in files:
	    try:
	        key = fp.split('_')[0]
		if dic.has_key(key):
		    dic[key].append(fp)
		else:
		    dic[key] = []
		    dic[key].append(fp)
	    except Exception as e:
	        print fp + ' generate map error: ' + str(e) 

def write_to_file(file_name, dic):
    with codecs.open(file_name, 'w+', encoding='utf-8') as f:
	f.write(json.dumps(dic))


def main():
    dic = OrderedDict()
    generate_map('jibing_html', dic)
    write_to_file('jinbing_src_map.json', dic)


if __name__ == '__main__':
    main()






