#!/usr/bin/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
#from codecs import open

import lxml.etree as etree
 
error = False
parser = etree.XMLParser(encoding="utf-8")
tree = ET.parse('addons/survey_methodology_extra/data/questions.xml', parser=parser)
root = tree.getroot()

colors = {
        'enabled': 'green',
        'disabled': 'blue',
        'closed': 'gray',
}

shapes = {
        'Null': 'none',
        'Variable': 'box',
        'View': 'Msquare',
}

with open('question.xml.ori', 'w') as fori:
        xml = ET.tostring(root, encoding="ascii")
        xml = re.sub(r'\s*\n\s*','\n', xml)
        fori.write(xml)

def norm(text):
        text = re.sub('\n+', '', text)
        text = text.strip()
        text = re.sub('\s+',' ',text)
        return text

def get_field(ele_record, name, text=None, ref=None, eval=None):
        field = (ele_record.findall('field[@name="%s"]'%name) or [ET.SubElement(ele_record, 'field', {'name':name})])[0]
        field.text = field.text or (text and text) or ''
        ref_or_eval = 'ref' in field.attrib or 'eval' in field.attrib
        if ref and not ref_or_eval: field.attrib['ref'] = ref
        if eval and not ref_or_eval: field.attrib['eval'] = eval
        field.text = norm(field.text)
        return field

node_set = set()
idnodes = {}
nodes = []
prelation = []
qrelation = []
last_variable_enabled = None

for ele_record in root.iter('record'):
        field = {}
        field['question'] = get_field(ele_record, 'question')
        field['name'] = get_field(ele_record, 'name')
        field['variable_name'] = get_field(ele_record, 'variable_name')
        field['note'] = get_field(ele_record, 'note')
        field['type'] = get_field(ele_record, 'type', text='View')
        field['format_id'] = get_field(ele_record, 'format_id')
        field['initial_state'] = get_field(ele_record, 'initial_state', text='disabled')
        field['survey_id'] = get_field(ele_record, 'survey_id', ref='survey_EE12')
        field['parent_id'] = get_field(ele_record, 'parent_id', ref='EE12')
        field['next_enable'] = get_field(ele_record, 'next_enable', eval='False')
        field['page'] = get_field(ele_record, 'page', text='1')

        field['code'] = get_field(ele_record, 'code')
        field['description'] = get_field(ele_record, 'description')

        complete_name = ele_record.attrib['id'].replace('_', ' / ')

        if field['name'].text not in ele_record.attrib['id']:
                if len(field['name'].text) > 0:
                        field['question'].text= field['name'].text
                field['name'].text  = ele_record.attrib['id'].split('_')[-1]

        if 'ref' in field['format_id'].attrib and field['format_id'].attrib['ref'] == 'format_Group':
                field['type'].text = 'View'
                del field['format_id'].attrib['ref']
                field['format_id'].attrib['eval'] = False
                field['initial_state'].text = 'closed'

        if field['type'].text not in ['None', 'Null', 'Variable', 'View']:

                if 'format_' in field['format_id'].text:
                        field['type'].text = 'Variable'

                if field['type'].text in ['Group']:
                        if 'ref' in field['format_id']:
                                del field['format_id'].attrib['ref']
                        field['format_id'].attrib['eval'] = 'False'
                        field['type'].text = 'View'
                        field['initial_state'].text = 'closed'

                if field['type'].text in ['Integer', 'Float']:
                        field['format_id'].attrib['ref'] = 'format_%s' % (field['format_id'].text)
                        del field['format_id'].attrib['eval']
                        field['format_id'].text = ''
                        field['type'].text = 'Variable'

        if len(field['variable_name'].text) < 3:
                field['variable_name'].text = ele_record.attrib['id']

        if len(field['note'].text) < 3:
                field['note'].text = field['question'].text

        ele_record.remove(field['code'])
        ele_record.remove(field['description'])
        if field['type'].text != 'Variable':
                field['next_enable'].text=None
                field['next_enable'].attrib['eval']='False'
                field['variable_name'].text=None
                field['variable_name'].attrib['eval']='False'
                field['format_id'].text=None
                field['format_id'].attrib['eval']='False'
        elif 'eval' in field['variable_name'].attrib and field['variable_name'].attrib['eval']=='False':
                field['variable_name'].text='_'.join(ele_record.attrib['id'].split('_')[1:])
                del field['variable_name'].attrib['eval']
        elif 'eval' not in field['variable_name'].attrib:
                field['variable_name'].text='_'.join(ele_record.attrib['id'].split('_')[1:])

        ff = []
        for f in ele_record:
                if f.text and 'ref' in f.attrib:
                        del f.attrib['ref']
                if f.text and 'eval' in f.attrib:
                        del f.attrib['eval']
                if 'eval' in f.attrib and 'ref' in f.attrib and f.attrib['eval'] not in ['None', 'False']:
                        del f.attrib['ref']
                if 'eval' in f.attrib and 'ref' in f.attrib and f.attrib['ref']:
                        del f.attrib['eval']
                ff.append(f.attrib['name'])

        if field['type'].text == 'Variable' and field['next_enable'].text == 'True:':
                if last_variable_enabled is not None:
                        print complete_name
                        last_variable_enabled.text = 'True:%s' % complete_name
                last_variable_enabled = field['next_enable']

        if complete_name in node_set:
                print "Repeated:", complete_name
                error = True
        else:
                node_set.add(complete_name)

        # Creo grafo
        nodes.append((complete_name, colors[field['initial_state'].text], shapes[field['type'].text]))
        idnodes[ele_record.attrib['id']] = complete_name
        if 'ref' in field['parent_id'].attrib:
                if not field['parent_id'].attrib['ref'] in idnodes:
                        print field['parent_id'].attrib['ref']
                else:
                        prelation.append((idnodes[field['parent_id'].attrib['ref']], complete_name))

        if field['type'].text == 'Variable':

                for line in field['next_enable'].text.split(';'):
                        action = line.split(':')
                        condition = action[0]

                        w_disable = action[2].split(',') if len(action) >= 3 else []

                        w_enable = action[1].split(',') if len(action) >= 2 else []

                        for name in w_enable:
                                qrelation.append((complete_name, name, condition, 'green'))

                        for name in w_disable:
                                qrelation.append((complete_name, name, condition, 'red'))

if error:
        import sys
        sys.exit(-1)


with open('question.xml.new', 'w') as fnew:
        xml = ET.tostring(root, encoding="ascii")
        xml = re.sub(r'\s*\n\s*','\n', xml)
        fnew.write(xml)


with open('question.dot', 'w') as fdot:
        fdot.write("digraph G {\n")
        fdot.write("rankdir=LR;\n")
        rank = {}
        for item, color, shape in nodes:
                rn = len(item.split('/'))
                if rn not in rank: rank[rn] = []
                rank[rn].append(item)
                fdot.write('"%s" [color="%s", shape="%s"];\n' % (item, color, shape))
        for item in prelation:
                fdot.write('"%s"->"%s" [weight="1"];\n' % item)
        for item in qrelation:
                fdot.write('"%s"->"%s" [label="%s", color="%s", weigth="1"];\n' % item)
        for item in rank.values():
                fdot.write('{ rank = same;\n\t"%s" };\n' % '";\n\t"'.join(item))
        fdot.write("};\n")
        fdot.close()

