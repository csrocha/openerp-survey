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
import tools
import time
import logging

_logger = logging.getLogger(__name__)

# Codigo JavaScript que permite Cambiar de <input/> con la tecla Enter.
_enter_js = """
<html>
<script type="text/javascript">
    $(document).ready(function(){
      (function(){
        var keyup_orig = openerp.instances.instance0.web.form.FieldChar.prototype.events.keyup;
        openerp.instances.instance0.web.form.FieldChar.prototype.events.keyup = function(e) {
            if (e.which === $.ui.keyCode.ENTER) {
                    textboxes = $("input:visible");
                    currentBoxNumber = textboxes.index(e.target);
                    if (textboxes[currentBoxNumber + 1] != null) {
                            nextBox = textboxes[currentBoxNumber + 1];
                            nextBox.focus();
                            nextBox.select();
                            e.preventDefault();
                            return false;
                    }
            }
        }
      })();
    });
</script>
</html>
"""

class questionnaire(osv.osv):
    """
    Este objeto presenta las preguntas de un cuestionario para un encuestado.
    """
    _name = 'survey_methodology.questionnaire'
    _inherit = [ _name ]

    _columns = {
        'actual_page': fields.integer('Actual Page', readonly=True),
    }

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

        answer_obj = self.pool.get('survey_methodology.answer')
        question_obj = self.pool.get('survey_methodology.question')
        question_ids = question_obj.search(cr, uid, [('complete_place','=',fields)])

        for question in question_obj.browse(cr, uid, question_ids):

            if question.next_enable == False:
                _logger.warning('Question %s no enable any other question' % question.complete_name)
                continue

            # Habilitación o deshabilitación de preguntas.
            for lines in question.next_enable.split('\n'):
                if lines.strip():
                    parsed = re.search(r'(?P<condition>[^:]*):(?P<to_enable>[^:]*)(:(?P<to_disable>.*))?', lines).groupdict()
                    if parsed['condition'] and eval(parsed['condition'], tools.local_dict(input_text, question)):
                        to_enable = filter(lambda i: i!='', (parsed['to_enable'] or '').split(','))
                        to_disable = filter(lambda i: i!='', (parsed['to_disable'] or '').split(','))
                        to_enable = [ to if ' / ' in to else to.replace('_', ' / ') for to in to_enable ]
                        to_disable = [ to if ' / ' in to else to.replace('_', ' / ') for to in to_disable ]
                        next_dict = dict(
                            [ (qid, 'enabled') for qid in question_obj.search(cr, uid, [
                                ('survey_id','=',question.survey_id.id),
                                ('complete_name', 'in', to_enable)
                            ]) ] +
                            [ (qid, 'disabled') for qid in question_obj.search(cr, uid, [
                                ('survey_id','=',question.survey_id.id),
                                ('complete_name', 'in', to_disable)
                            ]) ])
                        next_field_code = question_obj.read(cr, uid, next_dict.keys(), ['complete_place', 'complete_name'])
                        for item in next_field_code:
                            complete_place = item['complete_place']
                            value['sta_%s' % complete_place] = next_dict[item['id']]
                            it_ids = answer_obj.search(cr, uid, [('complete_place','=',complete_place)])
                            answer_obj.write(cr, uid, it_ids, {'state': next_dict[item['id']]})

            # Evaluamos el formato
            format_obj = question.format_id
            format_res = format_obj.evaluate(input_text, question)[format_obj.id]

            # Mensajes según pregunta.
            value['msg_%s' % fields] = format_res['message']
            value['vms_%s' % fields] = format_res['message']
            value['for_%s' % fields] = format_res['formated']
            value['vfo_%s' % fields] = format_res['formated']
            value['val_%s' % fields] = format_res['valid']

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

    def fields_view_get(self, cr, uid, view_id=None, view_type=None, context=None, toolbar=False, submenu=False):
        """
        Genera la vista dinámicamente, según las preguntas de la encuesta.
        """
        if context is None:
            context = {}
        questionnaire_id = context.get('questionnaire_id', context.get('actual_id', None))
        actual_page = context.get('actual_page',1)

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

        res = super(questionnaire, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar=toolbar, submenu=submenu)
        if view_type == "form" and questionnaire_id is not None:
            qaire_ids = self.search(cr, uid, [('id','=',questionnaire_id)])[:1]
            view_item = ['<group colspan="4" col="5">']

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
                            '<label string="" colspan="1"/>'
                            '<label string="%(name)s" colspan="1"/>'
                            '<label string="%(question)s" colspan="3"/>'
                            % item_map
                        )
                    if question.type=='View':
                        view_item.append(
                            '<h3>'
                            '<label string="%(complete_name)s" colspan="2"/>'
                            '</newline>'
                            '<label string="%(question)s" colspan="3"/>'
                            '</h3>'
                            % item_map
                        )
                    if question.type=='Variable':
                        view_item.append(
                            '<label string="%(complete_name)s" colspan="1"/>'
                            '<label string="%(question)s" colspan="1"/>'
                            '<field name="inp_%(complete_place)s" on_change="onchange_input(inp_%(complete_place)s, \'%(complete_place)s\')"'
                            ' modifiers="{&quot;readonly&quot;: [[&quot;sta_%(complete_place)s&quot;, &quot;not in&quot;, [&quot;enabled&quot;]]]}"'
                            ' nolabel="1" colspan="1"/>'
                            '<field name="vms_%(complete_place)s" modifiers="{&quot;readonly&quot;: true}" nolabel="1" colspan="1"/>'
                            '<field name="vfo_%(complete_place)s" modifiers="{&quot;readonly&quot;: true}" nolabel="1" colspan="1"/>'
                            '<field name="sta_%(complete_place)s" modifiers="{&quot;invisible&quot;: true}" nolabel="1" colspan="1"/>'
                            '<field name="msg_%(complete_place)s" modifiers="{&quot;readonly&quot;: false,&quot;invisible&quot;: true}"/>'
                            '<field name="val_%(complete_place)s" modifiers="{&quot;readonly&quot;: false,&quot;invisible&quot;: true}"/>'
                            '<field name="for_%(complete_place)s" modifiers="{&quot;readonly&quot;: false,&quot;invisible&quot;: true}"/>'
                            '<newline/>'% item_map
                        )
                    res['fields']['inp_%s' % question.complete_place] = {
                        'selectable': False,
                        'readonly': question.type != 'Variable',
                        'type': 'char',
                        'string': "%s" % (question.question),
                    }
                    res['fields']['msg_%s' % question.complete_place] = {
                        'selectable': False,
                        'readonly': True,
                        'type': 'char',
                        'string': 'Invisible Message',
                    }
                    res['fields']['vms_%s' % question.complete_place] = {
                        'selectable': False,
                        'readonly': True,
                        'type': 'char',
                        'string': 'Message',
                    }
                    res['fields']['sta_%s' % question.complete_place] = {
                        'selectable': False,
                        'readonly': True,
                        'type': 'char',
                        'string': 'Status',
                    }
                    res['fields']['for_%s' % question.complete_place] = {
                        'selectable': False,
                        'readonly': True,
                        'type': 'char',
                        'string': 'Invisible Formated',
                    }
                    res['fields']['vfo_%s' % question.complete_place] = {
                        'selectable': False,
                        'readonly': True,
                        'type': 'char',
                        'string': 'Formated',
                    }
                    res['fields']['val_%s' % question.complete_place] = {
                        'selectable': False,
                        'readonly': True,
                        'type': 'boolean',
                        'string': 'Valid',
                    }
            view_item.append('</group>')
            view_item.append(_enter_js)

            insert_view = """<group position="after"> <separator string="Page %i."/> %s </group>""" % (actual_page, ' '.join(view_item))
            source = etree.fromstring(encode(res['arch']))
            source = apply_inheritance_specs(source, insert_view, view_id)
            res.update(
                arch=etree.tostring(source)
            )
        return res

    def prev_page(self, cr, uid, ids, context=None):
        context = context or {}
        for q in self.browse(cr, uid, ids, context=None):
            actual_page = max(1, q.actual_page - 1)
            self.write(cr, uid, [q.id], {'actual_page': actual_page})
            context['questionnaire_id'] = q.id
            context['actual_page'] = actual_page
        return {
            'type': 'ir.actions.act_window',
            'name': 'Questtionary. page %i' % actual_page,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'survey_methodology.questionnaire',
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
            'name': 'Questtionary. page %i' % q.actual_page,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'survey_methodology.questionnaire',
            'res_id': context['questionnaire_id'],
            'context': context,
        }

    def next_page(self, cr, uid, ids, context=None):
        context = context or {}
        for q in self.browse(cr, uid, ids, context=context):
            actual_page = min(100, q.actual_page + 1)
            self.write(cr, uid, [q.id], {'actual_page': actual_page})
            context['questionnaire_id'] = q.id
            context['actual_page'] = actual_page
        return {
            'type': 'ir.actions.act_window',
            'name': 'Questtionary. page %i' % q.actual_page,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'survey_methodology.questionnaire',
            'res_id': context['questionnaire_id'],
            'context': context,
        }
    def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
        """
        Lee los campos a partir de las asnwer asociadas.
        """
        answer_obj = self.pool.get('survey_methodology.answer')
        question_obj = self.pool.get('survey_methodology.question')

        res = super(questionnaire, self).read(cr, uid, ids, fields=fields, context=context, load=load)

        for r in res:
            if 'survey_id' not in r:
                continue

            survey_id = r['survey_id']
            survey_id = survey_id if type(survey_id) is int else survey_id[0]

            a_ids = answer_obj.search(cr, uid, [ ('questionnaire_id','=',r['id']) ])
            # Creamos las preguntas si no existen.
            if a_ids == []:
                q_ids = question_obj.search(cr, uid, [('survey_id','=',survey_id)])
                for question in question_obj.browse(cr, uid, q_ids):
                    v = {
                        'name': question.question,
                        'complete_place': question.complete_place,
                        'code': question.name,
                        'input': False,
                        'formated': False,
                        'message': False,
                        'valid': False,
                        'questionnaire_id': r['id'],
                        'question_id': question.id,
                    #    'state': question.initial_state,
                    }
                    a_ids.append(answer_obj.create(cr, uid, v))
                    answer_obj.write(cr, uid, a_ids[-1], {'state': question.initial_state})
            # Leemos las preguntas.
            for answer in answer_obj.browse(cr, uid, a_ids):
                r['inp_%s' % answer.complete_place]=answer.input
                r['msg_%s' % answer.complete_place]=answer.message
                r['vms_%s' % answer.complete_place]=answer.message
                r['sta_%s' % answer.complete_place]=answer.state
                r['for_%s' % answer.complete_place]=answer.formated
                r['vfo_%s' % answer.complete_place]=answer.formated
                r['val_%s' % answer.complete_place]=answer.valid
        return res

    def write(self, cr, uid, ids, values, context=None):
        """
        Escribe los campos a las answers asociadas.
        """
        answer_obj = self.pool.get('survey_methodology.answer')
        question_obj = self.pool.get('survey_methodology.question')

        res = super(questionnaire, self).write(cr, uid, ids, values, context=context)

        answer_ids = answer_obj.search(cr, uid, [
            ('questionnaire_id','in',ids),
            ('complete_place','in',[key[4:] for key in values.keys() if key[3]=="_"])
        ])

        for answer in answer_obj.read(cr, uid, answer_ids, ['complete_place']):
            complete_place = answer['complete_place']
            v = {}

            if 'msg_%s' % complete_place in values: v.update(message=values['msg_%s' % complete_place])
            if 'sta_%s' % complete_place in values: v.update(state=values['sta_%s' % complete_place])
            if 'inp_%s' % complete_place in values: v.update(input=values['inp_%s' % complete_place])
            if 'for_%s' % complete_place in values: v.update(formated=values['for_%s' % complete_place])
            if 'val_%s' % complete_place in values: v.update(valid=values['val_%s' % complete_place])
            
            answer_obj.write(cr, uid, answer['id'], v)

        return True

questionnaire()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
