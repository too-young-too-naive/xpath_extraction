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


def get_title(tree):
    try:
        elements = get_element('//div[@class="wrap mt5"]/div[@class="jb-name fYaHei gre"]', tree)
        if len(elements) > 0:
            text = ''
            for x in elements:
                text += get_element('string(//*)', x)[0]
            text = cleanup(text)
            return text
        else:
            return ''
    except Exception as e:
        print 'get_title() Error: ' + str(e)
        return ''


def get_directory(tree):
    try:
        elements = get_element('//div[@class="wrap mt10 nav-bar"]', tree)
        if len(elements) > 0:
            text = ''
            for x in elements:
                text += get_element('string(//*)', x)[0]
            text = cleanup(text)
            return text
        else:
            return ''
    except Exception as e:
        print 'get_title() Error: ' + str(e)
        return ''


def get_introduction(tree):
    try:
        dic = OrderedDict()
        head = get_element('//div[@class="jib-articl fr f14 "]/div[@class="jib-articl-con jib-lh-articl"]/strong[@class="db f20 fYaHei fb jib-articl-tit tc pr"]/text()', tree)[0]
        summary = get_element('string(//div[@class="jib-articl fr f14 "]/div[@class="jib-articl-con jib-lh-articl"]/p)', tree)[0]
        if head and summary is not None:
            dic[head] = cleanup(summary) 
        elements = get_element('//div[@class="jib-articl fr f14 "]/div[@class="mt20 articl-know"]', tree)
        for div in elements:
            head2 = get_element('string(//strong)', div)
            details = get_element('//p', div)
            inner_dic = get_inner_slot(details)
            if head and summary is not None:
                dic[head2[0]] = inner_dic
        return dic
    except Exception as e:
        print 'get_introduction() Error: ' + str(e)
        return


def get_inner_slot(lists):
	try:
		if(len(lists)) == 1:
			return cleanup(get_element('string(//*)', lists[0])[0])
		else:
			dic = OrderedDict()
			for p in lists:
				head = get_element('string(//span[1])', p)
				value = get_element('string(//span[2])', p)
				if len(head)!=0 and len(value)!=0:
					dic[head[0][:-1]] = cleanup(value[0])
			return dic
	except Exception as e:
		print 'get_inner_slot() Error: ' + str(e) 


def get_reason(tree):
    try:
        text = get_element('string(//div[@class="jib-janj bor clearfix"]/div[@class=" jib-articl fr f14 jib-lh-articl"])', tree)[0]
        return cleanup(text)
    except Exception as e:
        print 'get_reason() Error: ' + str(e)
        return


def get_precaution(tree):
    try:
        elements = get_element('//div[@class="jib-janj bor clearfix"]/div[@class="jib-articl fr f14 jib-lh-articl"]/p', tree)
        if len(elements) > 0:
            text = ''
            for p in elements:
                text += get_element('string(//*)', p)[0]
            text = cleanup(text)
            return text
        else: 
            return ''
    except Exception as e:
        print 'get_precaution() Error: ' + str(e)
        return 

            
def get_neopathy(tree):
    try:
        elements = get_element('//div[@class="jib-janj bor clearfix"]/div[@class="jib-articl fr f14 jib-lh-articl"]', tree)
        text = ''
        # text += get_element('string(//span[@class="db f12 lh240 mb15 "])', elements)
        # text += get_element('string(//p)', elements)
        if len(elements) > 0:
        	for x in elements:
        		text += get_element('string(//*)', x)[0]
        # return text
        return cleanup(text)
    except Exception as e:
        print 'get_neopathy() Error: ' + str(e)
        return


def get_symptom(tree):
	try:
		elements = get_element('//div[@class="jib-janj bor clearfix"]/div[@class="jib-articl fr f14 jib-lh-articl"]', tree)
		if len(elements) > 0:
			text = ''
        	for p in elements:
        		text += get_element('string(//*)', p)[0]
        	text = cleanup(text)
        	return text
	except Exception as e:
		print 'get_symptom() Error: ' + str(e)
    	return


def get_inspection(tree):
	try:
		elements = get_element('//div[@class="jib-janj bor clearfix"]/div[@class="jib-articl fr f14 jib-lh-articl"]/p', tree)
		if len(elements) > 0:
			text = ''
			for p in elements:
				text += get_element('string(//*)', p)[0]
			return cleanup(text)
		else:
			return ''
	except Exception as e:
		print 'get_inspection() Error: ' + str(e)


def get_diagnosis(tree):
	try:
		elements = get_element('//div[@class="jib-janj bor clearfix"]/div[@class="jib-articl fr f14 jib-lh-articl"]', tree)
		if len(elements) > 0:
			text = ''
			for p in elements:
				text += get_element('string(//*)', p)[0]
			text = cleanup(text)
			return text
		else:
			return ''
	except Exception as e:
		print 'get_diagnosis() Error: ' + str(e)


def get_treatement(tree):
	try:
		elements = get_element('//div[@class="jib-janj bor clearfix"]/div[@class="jib-articl fr f14 "]', tree)
		if len(elements) > 0:
			text = ''
			for p in elements:
				text += get_element('string(//*)', p)[0]
			return cleanup(text)
		else:
			return ''
	except Exception as e:
		print 'get_treatement() Error: ' + str(e)


def get_nurse(tree):
	try:
		elements = get_element('//div[@class="jib-janj bor clearfix"]/div[@class="jib-articl fr f14 jib-lh-articl"]//p', tree)
		if len(elements) > 0:
			text = ''
			for p in elements:
				text += get_element('string(//*)', p)[0]
			return cleanup(text)
		else:
			return ''
	except Exception as e:
		print 'get_nurse() Error: ' + str(e)


def get_diet(tree):
	try:
		dic = OrderedDict()
		keys = get_element('//ul[@class="diet-tab bor-bot pb5 clearfix"]/li/text()', tree)
		value_1 = get_element('string(//div[@class="panels mt10"]/div[@class="diet-item"])', tree)
		value_2 = get_element('string(//div[@class="diet-item none clearfix"]/div[@class="diet-good clearfix"]/div[@class="fl diet-good-txt"])', tree)
		value_3 = get_element('string(//div[@class="diet-item none"]/div[@class="diet-good clearfix"]/div[@class="fl diet-good-txt"])', tree)
		if len(keys) == 1:
			dic[keys[0]] = cleanup(value_1[0])
		elif len(keys) == 2:
			dic[keys[0]] = cleanup(value_1[0])
			dic[keys[1]] = cleanup(value_2[0])
		else:
			dic[keys[0]] = cleanup(value_1[0])
			dic[keys[1]] = cleanup(value_2[0])
			dic[keys[2]] = cleanup(value_3[0])
		return dic
	except Exception as e:
		print 'get_diet() Error: ' + str(e)
		return


def get_tushuojibing(tree):
	pass



options = { 'cause': get_reason,
			'diagnosis': get_diagnosis,
			'neopathy': get_neopathy,
			'symptom': get_symptom,
			'gaishu': get_introduction,
			'nursing': get_nurse,
			'prevent': get_precaution,
			'treat': get_treatement,
			'inspect': get_inspection,
			'food': get_diet,
			'tushuojibing': get_tushuojibing
			}




def cleanup(text):
    if text is None:
        return ''
    tmp0 = re.sub(' +', ' ', text)
    tmp1 = tmp0.strip().replace('\t', '').replace('\r', '')
    tmp2 = re.sub('\n +', '\n', tmp1)
    tmp3 = re.sub('\n+', '\n', tmp2)
    return tmp3


def read_map(map_file):
	with codecs.open(map_file, 'rt', encoding='utf-8') as f:
		index_map = json.load(f)
		return index_map


def concat_to_json(read_directory, write_directory, map_file):
	index_map = read_map(map_file)
	for index in index_map:
		if len(index_map[index]) < 10:
			continue
		write_file_path = write_directory + '/data_' + index + '.json'
		dic = OrderedDict()
		for node in sorted(index_map[index]):
			read_file_path = read_directory + '/' + node
			tree = extract_tree(read_file_path)
			key = node.split('.')[0].split('_')[-1]
			value = options[key](tree)
			if key == 'cause':
				dic['title'] = get_title(tree)
				dic['url'] = 'http://jib.xywy.com/il_sii_' + str(index) + '.htm'
				dic['directory'] = get_directory(tree)
			dic[key] = value
		with codecs.open(write_file_path, 'w+', encoding='utf-8') as f:
			f.write(json.dumps(dic, ensure_ascii=False))
			print str(index)




def main():
	concat_to_json('jibing_html', 'jibing_data', 'jibing_src_map.json')
	# tree_introduction = extract_tree('test/1_gaishu.json')
	# introduction = get_introduction(tree_introduction)

	# tree_cause = extract_tree('test/1_cause.json')
	# cause = get_reason(tree_cause)

	# tree_symptom = extract_tree('test/1_symptom.json')
	# symptom = get_symptom(tree_symptom)

	# tree_diagnosis = extract_tree('test/1_diagnosis.json')
	# diagnosis = get_diagnosis(tree_diagnosis)

	# tree_precaution = extract_tree('test/1_prevent.json')
	# precaution = get_precaution(tree_precaution)

	# tree_neopathy = extract_tree('test/1_neopathy.json')
	# neopathy = get_neopathy(tree_neopathy)

	# tree_inspection = extract_tree('test/1_inspect.json')
	# inspection = get_inspection(tree_inspection)

	# tree_treatement = extract_tree('test/1_treat.json')
	# treatement = get_treatement(tree_treatement)

	# tree_nurse = extract_tree('test/1_nursing.json')
	# nurse = get_nurse(tree_nurse)

	# tree_diet = extract_tree('test/1_food.json')
	# diet = get_diet(tree_diet)

	
	# print introduction
	# print cause
	# print diagnosis
	# print precaution
	# print neopathy
	# print inspection
	# print treatement
	# print nurse
	# print diet
	# print symptom


if __name__ == '__main__':
	main()




