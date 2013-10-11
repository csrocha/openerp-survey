# -*- coding: utf-8 -*-
##############################################################################
#
#    Survey Methodology
#    Copyright (C) 2013 Coop. Trab. Moldeo Interactive Ltda.
#    No email
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import re
import netsvc
from osv import osv, fields
from lxml import etree
from openerp.tools import SKIPPED_ELEMENT_TYPES
from openerp.tools.translate import _
import tools
import time
from datetime import datetime
import logging
import os.path

from wizard.questionnaire_export import dump_inputs 

from openerp.osv.orm import setup_modifiers

_logger = logging.getLogger(__name__)

# ---- Codigo de orm.py : AQUI EMPIEZA. Permite generar vista por herencia. ----
def encode(s):
    if isinstance(s, unicode):
        return s.encode('utf8')
    return s

def raise_view_error(error_msg, child_view_id):
    view, child_view = self.pool.get('ir.ui.view').browse(cr, uid, [view_id, child_view_id], context)
    error_msg = error_msg % {'parent_xml_id': view.xml_id}
    raise AttributeError("View definition error for inherited view '%s' on model '%s': %s"
                         %  (child_view.xml_id, self._name, error_msg))

def locate(source, spec):
    """ Locate a node in a source (parent) architecture.

    Given a complete source (parent) architecture (i.e. the field
    `arch` in a view), and a 'spec' node (a node in an inheriting
    view that specifies the location in the source view of what
    should be changed), return (if it exists) the node in the
    source view matching the specification.

    :param source: a parent architecture to modify
    :param spec: a modifying node in an inheriting view
    :return: a node in the source matching the spec

    """
    if spec.tag == 'xpath':
        nodes = source.xpath(spec.get('expr'))
        return nodes[0] if nodes else None
    elif spec.tag == 'field':
        # Only compare the field name: a field can be only once in a given view
        # at a given level (and for multilevel expressions, we should use xpath
        # inheritance spec anyway).
        for node in source.getiterator('field'):
            if node.get('name') == spec.get('name'):
                return node
        return None

    for node in source.getiterator(spec.tag):
        if isinstance(node, SKIPPED_ELEMENT_TYPES):
            continue
        if all(node.get(attr) == spec.get(attr) \
                for attr in spec.attrib
                    if attr not in ('position','version')):
            # Version spec should match parent's root element's version
            if spec.get('version') and spec.get('version') != source.get('version'):
                return None
            return node
    return None

def intercalate(a, L):
    """
    Intercalate a beetween elements of L
    """
    if len(L)>0:
        for j in L[:-1]:
            yield j
            yield a
        yield L[-1]

def apply_inheritance_specs(source, specs_arch, inherit_id=None):
    """ Apply an inheriting view.

    Apply to a source architecture all the spec nodes (i.e. nodes
    describing where and what changes to apply to some parent
    architecture) given by an inheriting view.

    :param source: a parent architecture to modify
    :param specs_arch: a modifying architecture in an inheriting view
    :param inherit_id: the database id of the inheriting view
    :return: a modified source where the specs are applied

    """
    specs_tree = etree.fromstring(encode(specs_arch))
    # Queue of specification nodes (i.e. nodes describing where and
    # changes to apply to some parent architecture).
    specs = [specs_tree]

    while len(specs):
        spec = specs.pop(0)
        if isinstance(spec, SKIPPED_ELEMENT_TYPES):
            continue
        if spec.tag == 'data':
            specs += [ c for c in specs_tree ]
            continue
        node = locate(source, spec)
        if node is not None:
            pos = spec.get('position', 'inside')
            if pos == 'replace':
                if node.getparent() is None:
                    source = copy.deepcopy(spec[0])
                else:
                    for child in spec:
                        node.addprevious(child)
                    node.getparent().remove(node)
            elif pos == 'attributes':
                for child in spec.getiterator('attribute'):
                    attribute = (child.get('name'), child.text and child.text.encode('utf8') or None)
                    if attribute[1]:
                        node.set(attribute[0], attribute[1])
                    else:
                        del(node.attrib[attribute[0]])
            else:
                sib = node.getnext()
                for child in spec:
                    if pos == 'inside':
                        node.append(child)
                    elif pos == 'after':
                        if sib is None:
                            node.addnext(child)
                            node = child
                        else:
                            sib.addprevious(child)
                    elif pos == 'before':
                        node.addprevious(child)
                    else:
                        raise_view_error("Invalid position value: '%s'" % pos, inherit_id)
        else:
            attrs = ''.join([
                ' %s="%s"' % (attr, spec.get(attr))
                for attr in spec.attrib
                if attr != 'position'
            ])
            tag = "<%s%s>" % (spec.tag, attrs)
            if spec.get('version') and spec.get('version') != source.get('version'):
                raise_view_error("Mismatching view API version for element '%s': %r vs %r in parent view '%%(parent_xml_id)s'" % \
                                    (tag, spec.get('version'), source.get('version')), inherit_id)
            raise_view_error("Element '%s' not found in parent view '%%(parent_xml_id)s'" % tag, inherit_id)

    return source
# ---- Codigo de orm.py : AQUI TERMINA ----

class JavaScript:
    def __init__(self, script):
        self.script = script

    def __repr__(self):
        return self.script

# Codigo JavaScript que permite Cambiar de <input/> con la tecla Enter.
_enter_js = """
<html>
<script type="text/javascript">
	function sleep(ms)
	{
		var dt = new Date();
		dt.setTime(dt.getTime() + ms);
		while (Math.max(new Date().getTime(), dt.getTime()) == dt.getTime());
	};
    $(document).ready(function(){
      (function(){
        var char_keyup_orig = openerp.instances.instance0.web.form.FieldChar.prototype.events.keyup;
        openerp.instances.instance0.web.form.FieldChar.prototype.events.keyup = function(e) {
            if (e.which === $.ui.keyCode.ENTER) {
                    setTimeout(function() {
                        textboxes = $("input:visible:enabled");
                        currentBoxNumber = textboxes.index(e.target);
                        if (textboxes[currentBoxNumber + 1] != null) {
                                nextBox = textboxes[currentBoxNumber + 1];
                                nextBox.focus();
                                nextBox.select();
                                e.preventDefault();
                                return false;
                        }
                   }, 500);
            }
        }
      })();
    });
</script>
</html>
"""
_enter_js = """
<html>
<script type="text/javascript">
    $(document).ready(function(){
        debugger;
        sheets = $('.oe_form_sheetbg');
        main_sheet = sheets[sheets.length-1];
        main_sheet.className = 'oe_form_sheetbg survey_full';
    });
</script>
</html>"""

_enter_css_ = """
element.style {
display: block;
position: absolute;
width: 100%;
height: 100%;
background-color: white;
z-index: 10000;
left: 0px;
top: 0px;
}
"""

class questionnaire(osv.osv):
    """
    Este objeto presenta las preguntas de un cuestionario para un encuestado.
    """
    _name = 'sondaggio.questionnaire'
    _inherit = [ _name ]

    def get_parameters(self, cr, uid, ids, field_name, arg, context=None):
        if field_name[:4] != 'par_':
            return {}
        param_obj = self.pool.get('sondaggio.parameters')
        res = {}
        for q in self.browse(cr, uid, ids, context=context):
            p_l = [ par.value for par in q.parameter_ids if par.name == field_name[4:] ]
            res[q.id] = p_l[0] if p_l else False
        return res

    def search_parameters(self, cr, uid, obj, name, args, context):
        param_obj = self.pool.get('sondaggio.parameter')

        args =  [ item for sublist in [[('name','=',p[4:]), ('value', o, v)] for p,o,v in args ] for item in sublist ]

        p_ids = param_obj.search(cr, uid, args, context=context)
        p_reads = param_obj.read(cr, uid, p_ids, ['questionnaire_id'])
        p_ids = [ p['questionnaire_id'][0] for p in p_reads ]

        return [ ('id', 'in', p_ids) ]

    def get_url(self, cr, uid, ids, field_name, arg, context=None):
        user_obj = self.pool.get('res.users')    
        user_id = context.get('user_id', uid)
        user = user_obj.browse(cr, uid, user_id, context=context)
        login = user.login
        password = user.password

        r = {}
        base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url', default='', context=context)
        for questionnaire in self.browse(cr, uid, ids, context=context):
            r[questionnaire.id] = '%s/login?db=%s&login=%s&key=%s#action=questionnaire.ui&active_id=%s&active_code=%s'%(base_url, cr.dbname,login,password,questionnaire.id,questionnaire.code)
        return r

    def get_communication_date(self, cr, uid, ids, field_name, arg, context=None):
        r = {}
        for questionnaire in self.browse(cr, uid, ids, context=context):
            r[questionnaire.id] = max([ c.send_date for c in questionnaire.communication_batch_ids ]) if questionnaire.communication_batch_ids else False
        return r

    def get_num_communications(self, cr, uid, ids, field_name, arg, context=None):
        r = {}
        for questionnaire in self.browse(cr, uid, ids, context=context):
            r[questionnaire.id] = len(questionnaire.communication_batch_ids) if questionnaire.communication_batch_ids else False
        return r

    def get_date(self, cr, uid, ids, field_name, arg, context=None):
        if field_name[:5] != 'date_':
            return {}
        r = {}
        for questionnaire in self.browse(cr, uid, ids, context=context):
            messages = [ (m.date, m.body) for m in questionnaire.message_ids if field_name[5:] in m.body.lower() ]
            r[questionnaire.id] = messages[0][0] if messages else False
        return r


    _columns = {
        'actual_page': fields.integer('Actual Page', readonly=True),
        'url': fields.function(get_url, method=True, string='URL', readonly=True, type='char'),
        'fecha_ver': fields.char('Questionnaire group', size=16),
        'par_razon_social': fields.function(get_parameters, method=True, string='Razón social',
                                      readonly=True, type='text', fnct_search=search_parameters, store=True),
        'par_razon_social_ver': fields.function(get_parameters, method=True, string='Razón social verificada',
                                      readonly=True, type='text', fnct_search=search_parameters, store=True),
        'par_estrato_f': fields.function(get_parameters, method=True, string='Estrato',
                                      readonly=True, type='text', fnct_search=search_parameters, store=True),
        'par_muesorig': fields.function(get_parameters, method=True, string='Muestra Orig',
                                      readonly=True, type='text', fnct_search=search_parameters, store=True),
        'par_fecha_ver': fields.function(get_parameters, method=True, string='Fecha verificación',
                                      readonly=True, type='text', fnct_search=search_parameters, store=True),
        'par_fecha_env': fields.function(get_parameters, method=True, string='Fecha envío',
                                      readonly=True, type='text', fnct_search=search_parameters, store=True),
        'par_encuestador': fields.function(get_parameters, method=True, string='Encuestador',
                                      readonly=True, type='text', fnct_search=search_parameters, store=True),
        'last_communication_date': fields.function(get_communication_date, method=True, string='Fecha de comunicación',
                                                   readonly=True, type='date', store=False),
        'num_communications': fields.function(get_num_communications, method=True, string='Number of communications',
                                                   readonly=True, type='integer', store=False),
        'date_draft': fields.function(get_date, method=True, string='Date in Draft',
                                      readonly=True, type='datetime', store=False),
        'date_in_process': fields.function(get_date, method=True, string='Date in Process',
                                      readonly=True, type='datetime', store=False),
        'date_waiting': fields.function(get_date, method=True, string='Date in Waiting',
                                      readonly=True, type='datetime', store=False),
        'date_rejected': fields.function(get_date, method=True, string='Date Rejected',
                                      readonly=True, type='datetime', store=False),
        'date_complete': fields.function(get_date, method=True, string='Date Complete',
                                      readonly=True, type='datetime', store=False),
        'date_validated': fields.function(get_date, method=True, string='Date Validated',
                                      readonly=True, type='datetime', store=False),
        'date_in_coding': fields.function(get_date, method=True, string='Date in Coding',
                                      readonly=True, type='datetime', store=False),
        'date_cancelled': fields.function(get_date, method=True, string='Date Cancelled',
                                      readonly=True, type='datetime', store=False),
        'mail_state': fields.related('sent_mail_id', 'state', type='selection',
                                    string="Last mail state",
                                    selection=[
                                        ('outgoing', 'Outgoing'),
                                        ('sent', 'Sent'),
                                        ('received', 'Received'),
                                        ('exception', 'Delivery Failed'),
                                        ('cancel', 'Cancelled'),
                                    ]),
    }

    _order = 'name asc, par_estrato_f asc'

    _defaults = {
        'actual_page': 1,
    }

    def onchange_input(self, cr, uid, ids, input_text, fields, context=None):
        """
        Esta función toma el cambio que ocurre en una celda input y
        actualiza el estado del próximo campo según lo que indique las
        condiciones del "next_enable" o próximo campo a habilitar.
        También verifica que mensaje tiene que enviarse al dataentry.
        """
        context = context or None
        value={}
        complete_place = False

        answer_obj = self.pool.get('sondaggio.answer')
        question_obj = self.pool.get('sondaggio.node')
        question_ids = question_obj.search(cr, uid, [('variable_name','=',fields)])

        #answer_id = answer_obj.search(cr, uid, [('complete_place','=',fields),('questionnaire_id','=',ids)])

        # Iterate over all hierarchical branch questions.
        #child_ids = question_ids
        #parent_ids = question_obj.search(cr, uid, [('child_ids', 'in', child_ids)])
        #while len(parent_ids)>0:
        #    child_ids = child_ids + parent_ids
        #    parent_ids = question_obj.search(cr, uid, [('child_ids', 'in', parent_ids)])
        #question_ids = child_ids

        for question in question_obj.browse(cr, uid, question_ids):

            # Habilitación o deshabilitación de preguntas.
            if question.next_enable == False:
                _logger.warning('Question %s no enable any other question' % question.complete_name)
            else:
                _logger.debug('Next enable: %s' % (question.next_enable))
                for lines in question.next_enable.split('\n'):
                    if lines.strip():
                        parsed = re.search(r'(?P<condition>[^:]*):(?P<to_enable>[^:]*)(:(?P<to_disable>.*))?', lines).groupdict()
                        if parsed['condition'] and eval(parsed['condition'], tools.local_dict(input_text, question)):
                            to_enable = filter(lambda i: i!='', (parsed['to_enable'] or '').split(','))
                            to_disable = filter(lambda i: i!='', (parsed['to_disable'] or '').split(','))
                            to_enable = [ to if ' / ' in to else to.replace('_', ' / ') for to in to_enable ]
                            to_disable = [ to if ' / ' in to else to.replace('_', ' / ') for to in to_disable ]
                            _logger.debug('Searching to enable: %s' % (','.join(to_enable)))
                            _logger.debug('Searching to disable: %s' % (','.join(to_disable)))
                            next_dict = dict(
                                [ (qid, 'enabled') for qid in question_obj.search(cr, uid, [
                                    ('survey_id','=',question.survey_id.id),
                                    ('complete_name', 'in', to_enable)
                                ]) ] +
                                [ (qid, 'disabled') for qid in question_obj.search(cr, uid, [
                                    ('survey_id','=',question.survey_id.id),
                                    ('complete_name', 'in', to_disable)
                                ]) ])
                            _logger.debug('Found: %s' % (next_dict))
                            next_field_code = question_obj.read(cr, uid, next_dict.keys(), ['complete_place', 'complete_name'])
                            for item in next_field_code:
                                variable_name = item['variable_name']
                                value['sta_%s' % variable_name] = next_dict[item['id']]
                                it_ids = answer_obj.search(cr, uid, [('name','=',variable_name)])
                                if it_ids == []:
                                    q_ids = question_obj.search(cr, uid, [('survey_id','=',question.survey_id.id),('variable_name','=',variable_name)])
                                    for nq in question_obj.browse(cr, uid, q_ids):
                                        v = {
                                            'name': nq.variable_name,
                                            'input': False,
                                            'formated': False,
                                            'message': False,
                                            'valid': False,
                                            'questionnaire_id': ids[0],
                                            'question_id': nq.id,
                                        }
                                        it_ids.append(answer_obj.create(cr, uid, v))
                                    if it_ids == []:
                                        raise osv.except_osv("Inestable Questionary", "Not answer associated to the next field. Communicate with the administrator.")
                                answer_obj.write(cr, uid, it_ids, {'state': next_dict[item['id']]})
                                _logger.debug('Change %s(%s) to %s' % (variable_name, it_ids, next_dict[item['id']]))

            # Evaluamos el formato
            format_obj = question.format_id
            format_res = format_obj.evaluate(input_text, question)[format_obj.id]

            # Mensajes según pregunta.
            value['msg_%s' % fields] = format_res['message']
            value['vms_%s' % fields] = format_res['message']
            value['for_%s' % fields] = format_res['formated']
            value['vfo_%s' % fields] = format_res['formated']
            value['val_%s' % fields] = format_res['is_valid']

        r = { 'value': value }
        if complete_place:
            r.update(grab_focus='inp_%s' % complete_place)

        return r

    def fields_get(self, cr, uid, fields=None, context=None):
        """
        Genera la lista de campos que se necesita para responder la encuesta.
        """
        context = context or {}
        questionnaire_id = context.get('questionnaire_id', context.get('actual_id', None))
        actual_page = context.get('actual_page',1)
        res = super(questionnaire, self).fields_get(cr, uid, fields, context)

        if questionnaire_id is not None:
            qaire_ids = self.search(cr, uid, [('id','=',questionnaire_id)])
            for qaire in self.browse(cr, uid, qaire_ids):
                for question in qaire.survey_id.question_ids:
                    if question.page != actual_page: 
                        continue
                    res["inp_%s" % question.complete_place] = {
                        'selectable': False,
                        'readonly': question.type != 'Variable',
                        'type': 'char',
                        'string': question.question,
                    }
                    res["msg_%s" % question.complete_place] = {
                        'selectable': False,
                        'readonly': False,
                        'type': 'char',
                        'string': 'Invisible Message',
                    }
                    res["vms_%s" % question.complete_place] = {
                        'selectable': False,
                        'readonly': False,
                        'type': 'char',
                        'string': 'Message',
                    }
                    res["sta_%s" % question.complete_place] = {
                        'selectable': False,
                        'readonly': False,
                        'type': 'char',
                        'string': 'Status',
                    }
                    res["for_%s" % question.complete_place] = {
                        'selectable': False,
                        'readonly': True,
                        'type': 'char',
                        'string': 'Invisible Formated',
                    }
                    res["vfo_%s" % question.complete_place] = {
                        'selectable': False,
                        'readonly': True,
                        'type': 'char',
                        'string': 'Formated',
                    }
                    res["val_%s" % question.complete_place] = {
                        'selectable': False,
                        'readonly': True,
                        'type': 'boolean',
                        'string': 'Valid',
                    }
        return res

    def _get_tracked_fields(self, cr, uid, updated_fields, context=None):
        r = super(questionnaire, self)._get_tracked_fields(cr, uid, updated_fields, context=context)
        ks = [ k for k in r.keys() if k[3] != '_' ]
        return dict( (k,v) for k,v in r.items() if k in ks )
   
    def fields_view_get_dataentry(self, cr, uid, questionnaire_id, actual_page):
        qaire_ids = self.search(cr, uid, [('id','=',questionnaire_id)])[:1]
        view_item = ['<group colspan="4" col="6">']
        fields = {}

        for qaire in self.browse(cr, uid, qaire_ids):
            level = 1
            for question in qaire.survey_id.question_ids:
                new_level = len(question.complete_place)/2
                if question.page != actual_page: 
                    continue
                if level < new_level:
                    level = new_level 
                elif level > new_level:
                    level = new_level 
                item_map = {
                    'name': question.name,
                    'complete_name': question.complete_name.replace(' ',''),
                    'complete_place': question.complete_place,
                    'question': question.question,
                    'readonly': question.type=="Variable" and question.initial_state=="enabled" and "false" or "true",
                }
                if question.type=='Null':
                    view_item.append(
                        '<label string="" colspan="1" class="sm_null"/>'
                        '<label string="%(name)s" colspan="1" class="sm_null"/>'
                        '<label string="%(question)s" colspan="3" class="sm_null"/>'
                        '<newline/>'
                        % item_map
                    )
                if question.type=='View':
                    view_item.append(
                        '<label string="%(complete_name)s" colspan="1" class="sm_view"/>'
                        '<label string="%(question)s" class="sm_view" colspan="4"/>'
                        '<newline/>'
                        % item_map
                    )
                if question.type=='Variable':
                    view_item.append(
                        '<label string="%(complete_name)s" colspan="1" class="sm_complete_name"/>'
                        '<label string="%(question)s" colspan="1" class="sm_question"/>'
                        '<field name="inp_%(complete_place)s" on_change="onchange_input(inp_%(complete_place)s, \'%(complete_place)s\')"'
                        ' modifiers="{&quot;readonly&quot;: [[&quot;sta_%(complete_place)s&quot;, &quot;not in&quot;, [&quot;enabled&quot;]]]}"'
                        ' nolabel="1" colspan="1" class="sm_input"/>'
                        '<field name="vms_%(complete_place)s" modifiers="{&quot;readonly&quot;: true}" nolabel="1" colspan="1" widget="text_html" class="sm_message"/>'
                        '<field name="vfo_%(complete_place)s" modifiers="{&quot;readonly&quot;: true}" nolabel="1" colspan="1" class="sm_formated"/>'
                        '<field name="val_%(complete_place)s" nolabel="1" modifiers="{&quot;readonly&quot;: [[&quot;vms_%(complete_place)s&quot;, &quot;in&quot;, [false, &quot;&quot;]]], &quot;invisible&quot;: false }" colspan="1"/>'
                        '<field name="sta_%(complete_place)s" modifiers="{&quot;invisible&quot;: true}" nolabel="1" colspan="1"/>'
                        '<field name="msg_%(complete_place)s" modifiers="{&quot;readonly&quot;: false,&quot;invisible&quot;: true}"/>'
                        '<field name="for_%(complete_place)s" modifiers="{&quot;readonly&quot;: false,&quot;invisible&quot;: true}"/>'
                        '<newline/>'% item_map
                    )
                fields['inp_%s' % question.complete_place] = {
                    'selectable': False,
                    'readonly': question.type != 'Variable',
                    'type': 'char',
                    'string': "%s" % (question.question),
                }
                fields['msg_%s' % question.complete_place] = {
                    'selectable': False,
                    'readonly': True,
                    'type': 'char',
                    'string': 'Invisible Message',
                }
                fields['vms_%s' % question.complete_place] = {
                    'selectable': False,
                    'readonly': True,
                    'type': 'char',
                    'string': 'Message',
                }
                fields['sta_%s' % question.complete_place] = {
                    'selectable': False,
                    'readonly': True,
                    'type': 'char',
                    'string': 'Status',
                }
                fields['for_%s' % question.complete_place] = {
                    'selectable': False,
                    'readonly': True,
                    'type': 'char',
                    'string': 'Invisible Formated',
                }
                fields['vfo_%s' % question.complete_place] = {
                    'selectable': False,
                    'readonly': True,
                    'type': 'char',
                    'string': 'Formated',
                }
                fields['val_%s' % question.complete_place] = {
                    'selectable': False,
                    'readonly': True,
                    'type': 'boolean',
                    'string': 'Valid',
                }
        view_item.append('</group>')
        view_item.append(_enter_js)

        view = """<group position="after"> <separator string="Page %i."/> %s </group>""" % (actual_page, ' '.join(view_item))
        return view, fields

    def fields_view_get_callcenter(self, cr, uid, questionnaire_id, actual_page=None):
        qaire_ids = self.search(cr, uid, [('id','=',questionnaire_id)])[:1]
        view_item = ['<group colspan="4" col="6">']
        fields = {}
        types = {
            'Char': 'char',
            'Boolean': 'boolean',
            'Select one': 'selection',
        }
        for qaire in self.browse(cr, uid, qaire_ids):
            level = 1
            parameters = dict((p.name, p.value) for p in qaire.parameter_ids)
            for question in qaire.survey_id.question_ids:
                new_level = len(question.complete_place)/2
                if actual_page is None or question.page != actual_page: 
                    continue
                if level < new_level:
                    level = new_level 
                elif level > new_level:
                    level = new_level 
                item_map = {
                    'name': question.name,
                    'complete_name': question.complete_name.replace(' ',''),
                    'complete_place': question.complete_place,
                    'question': question.question,
                    'readonly': question.type=="Variable" and question.initial_state=="enabled" and "false" or "true",
                }
                if question.type=='View':
                    view_item.append(
                        #'<label string="%(complete_name)s" colspan="1" class="sm_view"/>'
                        '<label string="%(question)s" class="sm_view" colspan="4"/>'
                        '<newline/>'
                        % item_map
                    )
                if question.type=='Null':
                    view_item.append(
                        #'<label string="" colspan="1" class="sm_null"/>'
                        #'<label string="%(name)s" colspan="1" class="sm_null"/>'
                        '<label string="%(question)s" colspan="1" class="sm_null"/>'
                        '<newline/>'
                        % item_map
                    )
                if question.type=='Variable':
                    enable_conditions = []
                    # Indico en que estado debe estar habilitada la entrada.
                    if question.enable_in:
                        enable_conditions.append('|')
                        enable_conditions.append([ 'state', '!=', question.enable_in.encode('ascii')])
                    # Armo las condiciones de control.
                    if question.enable_condition_ids:
                        for c in question.enable_condition_ids[:-1]:
                            enable_conditions.append('&amp;')
                            enable_conditions.append(['inp_{0}'.format(c.operated_node_id.complete_place), c.operator.encode('utf8'), JavaScript(c.value)])
                        c = question.enable_condition_ids[-1]
                        enable_conditions.append(['inp_{0}'.format(c.operated_node_id.complete_place), c.operator.encode('utf8'), JavaScript(c.value)])
                    else:
                        # Le quito la operación OR que es una operación binaria.
                        enable_conditions = enable_conditions[1:]
                    # Compilo las condiciones.
                    rep_enable_conditions = repr(enable_conditions).replace('\'','&quot;').replace('"','&quot;')
                    item_map['enable_condition'] = 'modifiers="{{&quot;readonly&quot;: {0!s}}}"'.format(rep_enable_conditions) if rep_enable_conditions else ""
                    view_item.append(
                       # '<label string="%(complete_name)s" colspan="1" class="sm_complete_name"/>'
                        '<label for="inp_%(complete_place)s" colspan="3" class="sm_complete_name"/>'
                       # '<label string="" colspan="1"/>'
                        '<field name="inp_%(complete_place)s"'
                        '       colspan="3"'
                        '       class="sm_input"'
                        '       nolabel="1"'
                        '       %(enable_condition)s/>'
                        % item_map
                    )
                    # Si no todos los parámetros fueron resueltos no
                    # se resuelven todos los parámetros.
                    try:
                        f_string = question.question.format(**parameters)
                    except:
                        f_string = question.question

                    # Declaro el campo.
                    fields['inp_%s' % question.complete_place] = {
                        'selectable': False,
                        'readonly': question.type != 'Variable',
                        'type': types.get(question.format_id.name, 'char'),
                        'string': f_string,
                    }
                    # Si es de tipo selection agrego las opciones
                    if types.get(question.format_id.name, 'char') == 'selection':
                        fields['inp_%s' % question.complete_place]['selection'] = [ (q.name, q.question) for q in question.child_ids if q.type == 'Null' ]
        view_item.append('</group>')
        view_item.append(_enter_js)

        view = """
            <group id="body" position="inside">
            <separator string="%s."/>
            <newline/>
            %s
            </group>""" % ((actual_page and "Page %i" % actual_page) or "No Page", '\n'.join(view_item))
        _logger.debug(view)
        return view, fields

    def fields_view_get(self, cr, uid, view_id=None, view_type=None, context=None, toolbar=False, submenu=False):
        """
        Genera la vista dinámicamente, según las preguntas de la encuesta.
        """
        if context is None:
            context = {}
        questionnaire_id = context.get('questionnaire_id', context.get('actual_id', None))
        actual_page = context.get('actual_page',1)
        res = super(questionnaire, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar=toolbar, submenu=submenu)

        # En la primera vista, como es genérica para cualquier cuestionario, no vamos a tener la información
        # de como se cargan los datos. Es por ello que va a aparecer sin el cuestionario. Una vez que sepamos
        # cual es la encuesta, podemos completar el formulario.
        if view_type == "form" and questionnaire_id is not None:
            source = etree.fromstring(encode(res['arch']))
            #insert_view, insert_fields = self.fields_view_get_dataentry(cr, uid, questionnaire_id, actual_page)
            insert_view, insert_fields = self.fields_view_get_callcenter(cr, uid, questionnaire_id, actual_page=None)
            res['fields'].update(insert_fields)
            source = apply_inheritance_specs(source, insert_view, view_id)
            res.update(
                arch=etree.tostring(source)
            )
        return res

    def prev_page(self, cr, uid, ids, context=None):
        context = context or {}
        for q in self.browse(cr, uid, ids, context=None):
            cr.execute('SELECT MAX(Q.page) FROM sondaggio_answer AS A '
                       ' LEFT JOIN sondaggio_node AS Q ON A.question_id=Q.id '
                       'WHERE A.questionnaire_id = %s '
                       '  AND Q.page < %s '
                       '  AND A.state = \'enabled\'', (q.id, q.actual_page))
            next_page = cr.fetchall()
            if next_page and next_page > q.actual_page:
            	actual_page = next_page[0][0]
            self.write(cr, uid, [q.id], {'actual_page': actual_page})
            context['questionnaire_id'] = q.id
            context['actual_page'] = actual_page
        return {
            'type': 'ir.actions.act_window',
            'name': 'Questionary.%s' % ( actual_page and ' Page %i' % actual_page or ''),
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_model': 'sondaggio.questionnaire',
            'res_id': context['questionnaire_id'],
            'context': context,
        }

    def refresh_page(self, cr, uid, ids, context=None):
        context = context or {}
        for q in self.browse(cr, uid, ids, context=context):
            actual_page = q.actual_page
            context['questionnaire_id'] = q.id
            context['actual_page'] = actual_page
        return {
            'type': 'ir.actions.act_window',
            'name': 'Questionary.%s' % ( actual_page and ' Page %i' % actual_page or ''),
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_model': 'sondaggio.questionnaire',
            'res_id': context['questionnaire_id'],
            'context': context,
        }

    def next_page(self, cr, uid, ids, context=None):
        context = context or {}
        for q in self.browse(cr, uid, ids, context=context):
            cr.execute('SELECT MIN(Q.page) FROM sondaggio_answer AS A '
                       ' LEFT JOIN sondaggio_node AS Q ON A.question_id=Q.id '
                       'WHERE A.questionnaire_id = %s '
                       '  AND Q.page > %s '
                       '  AND A.state = \'enabled\'', (q.id, q.actual_page))
            next_page = cr.fetchall()
            if next_page and next_page > q.actual_page:
            	actual_page = next_page[0][0]
            self.write(cr, uid, [q.id], {'actual_page': actual_page})
            context['questionnaire_id'] = q.id
            context['actual_page'] = actual_page
        return {
            'type': 'ir.actions.act_window',
            'name': 'Questionary.%s' % ( actual_page and ' Page %i' % actual_page or ''),
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_model': 'sondaggio.questionnaire',
            'res_id': context['questionnaire_id'],
            'context': context,
        }

    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        """
        Lee los campos a partir de las asnwer asociadas.
        """
        answer_obj = self.pool.get('sondaggio.answer')
        question_obj = self.pool.get('sondaggio.node')

        res = super(questionnaire, self).read(cr, uid, ids, fields=fields, context=context, load=load)

        for r in res:
            if 'survey_id' not in r:
                continue

            survey_id = r['survey_id']
            survey_id = survey_id if type(survey_id) is int else survey_id[0]

            a_ids = answer_obj.search(cr, uid, [ ('questionnaire_id','=',r['id']) ])
            # Creamos las preguntas si no existen.
            if a_ids == []:
                q_ids = question_obj.search(cr, uid, [('survey_id','=',survey_id), ('variable_name','!=','')])
                for question in question_obj.browse(cr, uid, q_ids):
                    v = {
                        'name': question.variable_name,
                        'input': False,
                        'formated': False,
                        'message': False,
                        'valid': False,
                        'questionnaire_id': r['id'],
                        'question_id': question.id,
                    }
                    _logger.debug("Creating: %s", v)
                    a_ids.append(answer_obj.create(cr, uid, v))
                    answer_obj.write(cr, uid, a_ids[-1], {'state': question.initial_state})
            # Leemos las preguntas.
            for answer in answer_obj.browse(cr, uid, a_ids):
                r['inp_%s' % answer.name]=answer.input
                r['msg_%s' % answer.name]=answer.message
                r['vms_%s' % answer.name]=answer.message
                r['sta_%s' % answer.name]=answer.state
                r['for_%s' % answer.name]=answer.formated
                r['vfo_%s' % answer.name]=answer.formated
                r['val_%s' % answer.name]=answer.valid
        return res

    def is_valid(self, cr, uid, ids, values, context=None):
        for i in [ i for i in values.keys() if 'in_' in  i ]:
            import pdb; pdb.set_trace()
        return True

    def write(self, cr, uid, ids, values, context=None):
        """
        Escribe los campos a las answers asociadas.
        """
        answer_obj = self.pool.get('sondaggio.answer')
        question_obj = self.pool.get('sondaggio.node')

        res = super(questionnaire, self).write(cr, uid, ids, values, context=context)

        if self.is_valid(cr, uid, ids, values, context=None):

            answer_ids = answer_obj.search(cr, uid, [
                ('questionnaire_id','in',ids),
                ('name','in',[key[4:] for key in values.keys() if key[3]=="_"])
            ])

            for answer in answer_obj.read(cr, uid, answer_ids, ['name']):
                variable_name = answer['name']
                v = {}

                if 'msg_%s' % variable_name in values: v.update(message  = values['msg_%s' % variable_name])
                if 'sta_%s' % variable_name in values: v.update(state    = values['sta_%s' % variable_name])
                if 'inp_%s' % variable_name in values: v.update(input    = values['inp_%s' % variable_name])
                if 'for_%s' % variable_name in values: v.update(formated = values['for_%s' % variable_name])
                if 'val_%s' % variable_name in values: v.update(valid    = values['val_%s' % variable_name])
                
                answer_obj.write(cr, uid, answer['id'], v)

            return True

        else:

            return False

    def on_open_ui(self, cr, uid, ids, context=None):
        context = context or {}
        q = self.read(cr, uid, ids, ['code'])
        if q:
            context.update(
                active_id=q[0]['id'], 
                active_code=q[0]['code'], 
            )
        return {
            'type' : 'ir.actions.client',
            'name' : _('Start Questionnaire'),
            'tag' : 'questionnaire.ui',
            'context' : context
        }

    def on_open_online(self, cr, uid, ids, context=None):
        return self.on_open_ui(cr, uid, ids, context=dict(context, channel='online'))

    def on_open_offline(self, cr, uid, ids, context=None):
        return self.on_open_ui(cr, uid, ids, context=dict(context, channel='offline'))

    def on_open_telephonic(self, cr, uid, ids, context=None):
        return self.on_open_ui(cr, uid, ids, context=dict(context, channel='telephonic'))

    def on_open_personal(self, cr, uid, ids, context=None):
        return self.on_open_ui(cr, uid, ids, context=dict(context, channel='personal'))

    def on_open_mailing(self, cr, uid, ids, context=None):
        return self.on_open_ui(cr, uid, ids, context=dict(context, channel='mailing'))

    def exec_workflow_cr(self, cr, uid, ids, signal, context=None):
        wf_service = netsvc.LocalService("workflow")
        _logger.debug('Recibing signal %s for %s' % (signal, ids))
        for id in ids:
            wf_service.trg_validate(uid, self._name, id, signal, cr)
            data = self.read(cr, uid, id, ['state'])
        _logger.debug('Solve to state %s' % data['state'])
        return data['state']

    def do_backup(self, cr, uid, ids, state=None, context=None):
        """
        Append the rotated questionnaire in a file.
        """
        out_filename = "/tmp/questionnaire_bk.csv"
        header = not os.path.exists(out_filename)
        out_file = open(out_filename, 'a')

        _logger.info("Backup questionnaire. header=%s" % str(header))

        dump_inputs(cr, questionnaire_ids = ids, out_file=out_file, header=header, state=state)

        return True

    def onchange_survey_id(self, cr, uid, ids, survey_id):
        """
        Set list of parameters if any questionnaire in the same survey have defined parameters.
        """
        pars = []
        if survey_id:
            cr.execute("""
                       select P.name, '' as value
                       FROM sondaggio_questionnaire AS Q
                       LEFT JOIN sondaggio_parameter AS P ON (Q.id = P.questionnaire_id)
                       WHERE Q.survey_id=%s GROUP BY P.name;
                       """, (survey_id,))
            pars = cr.fetchall()
            pars = map(lambda (n,v): (0,0,dict(name=n,value=v)), pars)
        return {'value':{ 'parameter_ids': pars } }

    def onchange_parameter_ids(self, cr, uid, ids, parameter_ids, context=None):
        """
        Set fecha_ver when any parameter change questionnaire.
        """
        parameter_obj = self.pool.get('sondaggio.parameter')
        fecha_ver_id = parameter_obj.search(cr, uid, [('questionnaire_id','in',ids),('name','=','fecha_ver')])
        fecha_actual = datetime.now().strftime('%d%m%Y')

        if [ a for a,b,c in parameter_ids if b == 0 and 'name' in c and c['name'] == 'fecha_ver' ]:
            return {}

        if fecha_ver_id:
            # Cambiar la fecha con este ID
            parameter_ids = [ [a,b,c] for a,b,c in parameter_ids if b != fecha_ver_id[0] ]
            fecha_ver_action = parameter_ids + [[1,fecha_ver_id[0],{'value':fecha_actual}]]

        else:
            # Crear parametro fecha
            parameter_ids = [ [a,b,c] for a,b,c in parameter_ids if 'name' in c and c['name'] != 'fecha_ver' ]
            fecha_ver_action = parameter_ids + [[0,0,{'name':'fecha_ver', 'value':fecha_actual}]]

        print fecha_ver_action

        return {'value': { 'parameter_ids': fecha_ver_action } }

questionnaire()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
