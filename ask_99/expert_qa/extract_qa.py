# -*- coding: utf-8 -*-
from scrapy import Selector
import json
import codecs
import io
import os
import re
import logging
from collections import OrderedDict


def extract_tree(file_name):
    with codecs.open(file_name, 'rt', encoding='utf-8') as f:
        data = json.load(f)
        tree = data['content']
    return tree


def extract_url(file_name):
    with codecs.open(file_name, 'rt', encoding='utf-8') as f:
        data = json.load(f)
        url = data['url']
    return url


def get_element(path, tree):
    sel = Selector(text=tree)
    xp = lambda x: sel.xpath(x).extract()
    return xp(path)


def cleanup(text):
    if text is None:
        return ''
    tmp0 = re.sub(' +', ' ', text)
    tmp1 = tmp0.strip().replace('\t', '').replace('\r', '')
    tmp2 = re.sub('\n +', '\n', tmp1)
    tmp3 = re.sub('\n+', '\n', tmp2)
    return tmp3


def extract_normal(tree, dic):
    heads_details = get_element('//ul[@class="allubot"]/li', tree)
    if len(heads_details) == 0:
        return
    for head_detail in heads_details:
        head = get_element('string(//p[@class="qusdesc"])', head_detail)[0]
        detail = get_element('string(//p[@class="doctan"])', head_detail)[0]
        dic[cleanup(head)] = cleanup(detail)


def write_to_file(file_name, dic):
    with codecs.open(file_name, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(dic, ensure_ascii=False))


def concat_to_file(read_directory, write_directory):
    for (cur, dirs, files) in os.walk(read_directory):
        for fp in files:
            try:
                read_path = read_directory + '/' + fp
                tree = extract_tree(read_path)
                url = extract_url(read_path)
                dic = OrderedDict()
                dic['url'] = url
                extract_normal(tree, dic)
                print len(dic)
                if len(dic) == 1:
                    logging.warning('| ' + fp + ' | NO CONTENT!')
                    continue
                write_path = write_directory + '/data_' + fp
                write_to_file(write_path, dic)
                logging.info('| ' + fp + ' | EXTRACTED!')
            except Exception as e:
                print 'concate_to_file() Error: ' + str(e)
                print fp


def main():
    concat_to_file('expert_qa_html', 'expert_qa_data')


if __name__ == '__main__':
    main()