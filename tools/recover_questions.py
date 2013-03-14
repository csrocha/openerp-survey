#!/usr/bin/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re

import lxml.etree as etree
 
tree = ET.parse('addons/survey_methodology_extra/data/questions.xml')
root = tree.getroot()

with open('question.xml.ori', 'w') as fori:
        xml = ET.tostring(root, encoding="utf8")
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
        field['next_enable'] = get_field(ele_record, 'next_enable', text='True:')
        field['page'] = get_field(ele_record, 'page', text='1')

        field['code'] = get_field(ele_record, 'code')
        field['description'] = get_field(ele_record, 'description')

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

with open('question.xml.new', 'w') as fnew:
        xml = ET.tostring(root, encoding="utf8")
        xml = re.sub(r'\s*\n\s*','\n', xml)
        fnew.write(xml)


