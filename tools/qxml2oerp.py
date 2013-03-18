#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree as ET
import re
#from codecs import open

import lxml.etree as etree

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


def get_bread_crumb(question):
        parent = question.find('..')
        self = [ question.attrib['id'] ] if 'id' in question.attrib else []
        if parent:
                return get_bread_crumb(parent) + self
        else:
                return self


def translate(in_root):
        OERP = ET.Element('openerp')
        DATA = ET.SubElement(OERP, 'data')

        co_id = 0
        field = {}
        for ele_question in in_root.iter('question'):
                rec = ET.SubElement(DATA, 'record')
                #rec.attrib['id'] = '_'.join(get_bread_crumb(ele_question))
                rec.attrib['id'] = ele_question.attrib['id']
                rec.attrib['model'] = 'survey_methodology.question'
                values = dict( (name, ET.SubElement(rec, 'field'))
                              for name in ['name', 'question', 'variable_name', 'note', 'type', 'format_id',
                                           'parent_id', 'survey_id', 'next_enable', 'page', 'initial_state'] )
                for key, item in values.items():
                        item.attrib['name'] = key
                values['name'].text = ele_question.find('name').text
                values['question'].text = ele_question.find('text').text
                values['survey_id'].attrib['ref'] = 'survey_EE12'
                values['page'].text = ele_question.find('page').text

                variable_name = ele_question.find('variable')
                if variable_name is not None:
                        values['variable_name'].text = variable_name.text
                        values['type'].text = 'Variable'
                        values['format_id'].attrib['ref'] = ele_question.find('format').attrib['ref']
                        values['initial_state'].text = 'disabled'

                        nexts = []
                        for act in ele_question.findall('actions'):
                                nexts.append('True:' + \
                                                ','.join([ a.attrib['ref'] for a in act.findall('enable') ]) + \
                                                ':' + \
                                                ','.join([ a.attrib['ref'] for a in act.findall('disable') ]))
                        values['next_enable'].text = ';'.join(nexts)
                elif ele_question.find('.//question') is not None:
                        values['type'].text = 'View'
                        values['initial_state'].text = 'closed'
                else:
                        values['type'].text = 'Null'
                        values['initial_state'].text = 'closed'

                if ele_question.attrib['id'] == "EE12_E_32_1_1":
                        import pdb; pdb.set_trace()
                parent=ele_question.find('../[@id]')
                if parent is not None:
                        values['parent_id'].attrib['ref'] = parent.attrib['id']

        return OERP

if __name__ == "__main__":
        infile = sys.argv[1]
        outfile = sys.stdout

        parser = etree.XMLParser(encoding="utf-8")
        tree = ET.parse(infile, parser=parser)
        in_root = tree.getroot()

        out_root = translate(in_root)

        ET.dump(out_root)


