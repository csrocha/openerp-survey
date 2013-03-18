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

def translate(in_root):
        Q = ET.Element('questionnaire')

        co_id = 0
        field = {}
        for ele_record in in_root.iter('record'):
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

                if 'eval' in field['parent_id'].attrib and field['parent_id'].attrib['eval'] == 'False':
                        p = Q
                else:
                        p_id = field['parent_id'].attrib['ref']
                        p = Q.findall(".//*[@id='%s']" % p_id)
                        if len(p)!=1:
                                import pdb; pdb.set_trace()
                        p = p[0]

                qu = ET.SubElement(p, 'question')
                qu.attrib['id'] = ele_record.attrib['id']
                te = ET.SubElement(qu, 'text')
                te.text = field['question'].text
                assert "%s" % field['name'].text in qu.attrib['id'].split('_')[-1], "Error: %s -- %s" % (field['name'].text, qu.attrib['id'])
                na = ET.SubElement(qu, 'name')
                na.text = field['name'].text
                pa = ET.SubElement(qu, 'page')
                pa.text = field['page'].text
                if len(field['variable_name'].text) > 0:
                        va = ET.SubElement(qu, 'variable')
                        va.text = field['variable_name'].text
                if 'ref' in field['format_id'].attrib:
                        fo = ET.SubElement(qu, 'format')
                        fo.attrib['ref'] = field['format_id'].attrib['ref']
                ist = ET.SubElement(qu, 'initial_state')
                ist.text = field['initial_state'].text
                qs = ET.SubElement(qu, 'actions')

        with_var = Q.findall(".//question[variable]")
        for q,nq in zip(with_var[:-1], with_var[1:]):
                qe = ET.SubElement(q.find('actions'), 'enable')
                qe.attrib['ref'] = nq.attrib['id']

        return Q

if __name__ == "__main__":
        infile = sys.argv[1]
        outfile = sys.stdout

        parser = etree.XMLParser(encoding="utf-8")
        tree = ET.parse(infile, parser=parser)
        in_root = tree.getroot()

        out_root = translate(in_root)

        ET.dump(out_root)


