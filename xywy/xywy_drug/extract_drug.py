# -*- coding: utf-8 -*-
from scrapy import Selector
import json
import codecs
import io
import os
import re
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


def cleanup_v1(text):
    if text is None:
        return ''
    tmp0 = re.sub(' +', ' ', text)
    tmp1 = tmp0.strip().replace('\t', '').replace('\r', '')
    tmp2 = re.sub('\n +', '\n', tmp1)
    tmp3 = re.sub('\n+', '\n', tmp2)
    return tmp3


def cleanup_v2(text):
    if text is None:
        return ''
    text = text.strip().replace('\t', '').replace('\r', '').replace('\n', '')
    return text


def get_title(tree):
    try:
        elements = get_element('//div[@class="p-inf fr mr20 mt20"]/h1[@class="f20 fYaHei fn mt20"]', tree)
        if len(elements) > 0:
            text = ''
            for x in elements:
                text += get_element('string(//*)', x)[0]
            text = cleanup_v2(text)
            return text
        else:
            return ''
    except Exception as e:
        print 'get_title() Error: ' + str(e)
        return ''


def get_directory(tree):
    try:
        elements = get_element('//ul[@class="p-inf-ul f14"]/li[1]/div[@class="fl mr10"]', tree)
        if len(elements) > 0:
            text = ''
            for x in elements:
                text += (get_element('string(//*)', x)[0] + ' ')
            text = cleanup_v1(text)
            return text
        else:
            return ''
    except Exception as e:
        print 'get_directory() Error: ' + str(e)
        return ''


def get_permit(tree):
    try:
        elements = get_element('//li[@class="li1 li2"]', tree)
        if len(elements) > 0:
            text = ''
            for x in elements:
                text += get_element('string(//*)', x)[0]
            text = cleanup_v2(text)
            return text
        else:
            return ''
    except Exception as e:
        print 'get_permit() Error: ' + str(e)
        return ''


def get_product_enterprise(tree):
    try:
        elements = get_element('//ul[@class="p-inf-ul f14"]/li[@class="li1"][1]', tree)
        if len(elements) > 0:
            text = ''
            for x in elements:
                text += get_element('string(//*)', x)[0]
            text = cleanup_v2(text)
            return text
        else:
            return ''
    except Exception as e:
        print 'get_product_enterprise() Error: ' + str(e)
        return ''


def get_related_illness(tree):
    try:
        elements = get_element('//ul[@class="p-inf-ul f14"]/li[@class="li1"][4]/div[@class="p-inf-ul-right p-inf-ul-jb fl"]/a', tree)
        if len(elements) > 0:
            text = ''
            for x in elements:
                text += (get_element('string(//*)', x)[0] + ' ')
            text = cleanup_v1(text)
            return text
        else:
            return ''
    except Exception as e:
        print 'get_related_illness() Error: ' + str(e)
        return ''



def get_instruction_book(tree):
	dic = OrderedDict()
	try:
		uls = get_element('//div[@class="clearfix pl20 pr20"]/ul', tree)
		for ul in uls:
			key = get_element('string(//li[1])', ul)[0]
			value = get_element('string(//li[2])', ul)[0]
			key = cleanup_v2(key).split(':')[0]
			value = cleanup_v1(value)
			dic[key] = value
		return dic
	except Exception as e:
		print 'get_instruction_book() Error: ' + str(e)
		return


def write_to_file(file_name, dic):
	with codecs.open(file_name, 'w+', encoding='utf-8') as f:
		f.write(json.dumps(dic, ensure_ascii=False))


def concat_to_json(read_directory, write_directory):
	for (cur, dirs, files) in os.walk(read_directory):
		for fp in files:
			try:
				dic = OrderedDict()
				tree = extract_tree(read_directory + '/' + fp)
				url = extract_url(read_directory + '/' + fp)
				title = get_title(tree)
				direct = get_directory(tree)
				permit = get_permit(tree)
				product_enterprise = get_product_enterprise(tree)
				related = get_related_illness(tree)
				instruction_book = get_instruction_book(tree)
				dic['title'] = title
				dic['url'] = url
				dic['directory'] = direct
				dic['drug_permit'] = permit[5: ]
				dic['product_enterprise'] = product_enterprise[5: ]
 				dic['related_illness'] = related
				dic['instruction_book'] = instruction_book
				file_name = write_directory + '/data_' + fp
				write_to_file(file_name, dic)
				print '| ' + 'data_' + fp + ' | has been saved' 
			except Exception as e:
				print 'concat_to_json() Error: ' + str(e)
				return

def main():
	concat_to_json('drug_html', 'drug_data')


if __name__ == '__main__':
	main()