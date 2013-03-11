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

class format(osv.osv):
    """"""
    _name = 'survey_methodology.format'
    _inherit = [ _name ]

    def evaluate(self, cr, uid, ids, input_text, question_id, context=None):
        import pdb; pdb.set_trace()

    def evaluation_test(self, cr, uid, ids, context=None):
        input_test_obj = self.pool.get('survey_methodology.input_test')
        question_obj = self.pool.get('survey_methodology.question')
        message_obj = self.pool.get('survey_methodology.message')
        fs = self.read(cr, uid, ids, ['validation', 'formating', 'message_ids', 'input_test_ids'])
        for f in fs:
            its = input_test_obj.read(cr, uid, f['input_test_ids'], ['name', 'question_id', 'formated', 'valid'])
            r = []
            v = True
            for it in its:
                question = question_obj.browse(cr, uid, it['question_id'][0]) if it['question_id'] else None
                r.append("<h2>Testing: %s</h2>" % it['name'])
                local_dict = {
                    'input': it['name'],
                    'linput': it['name'].lower(),
                    'uinput': it['name'].upper(),
                    'sinput': it['name'].strip(),
                    'slinput': it['name'].strip().lower(),
                    'suinput': it['name'].strip().upper(),
                    'inrange': lambda v, _min=None, _max=None: _min <= v and v < _max,
                    'self': question,
                    're': re,
                    'match': lambda regexp, _input: _input and re.match(regexp, _input.strip()) is not None,
                    'imatch': lambda regexp, _input: _input and re.match(regexp, _input.strip(), re.I) is not None,
                }
                try:
                    val_result = eval(f['validation'], local_dict)
                    for_result = eval(f['formating'], local_dict)
                    for msg in message_obj.read(cr, uid, f['message_ids'], ['name', 'condition']):
                        msg_result = eval(msg['condition'], local_dict)
                        if not type(msg_result) is bool:
                            v = False
                            r.append("<p><b>TypeError:</b> Expected Boolean result for validation.</p><p><b>Returned value is:</b> %s</p>" %
                                     type(val_result))
                        elif msg_result:
                            r.append("<p><b>Message raised:</b> %s</p>" % msg['name'])
                    if not type(val_result) is bool:
                        v = False
                        r.append("<p><b>TypeError:</b> Expected Boolean result for validation.</p><p><b>Returned value is:</b> %s</p>" %
                                 type(val_result))
                    if not type(for_result) in [ str, unicode ]:
                        v = False
                        r.append("<p><b>TypeError:</b> String result for format.</p><p><b>Returned value is:</b> %s</p>" %
                                 type(for_result))
                except SyntaxError as e:
                    r.append("<p><b>Syntax Error</b>: %s</p>\n<p><b>line:</b> %i, <b>character:</b> %i</p><p><b>code:</b> %s</p>" %
                             (e.args[0], e.args[1][1], e.args[1][2], e.args[1][3]))
                    v = False
                    r.append("<p>Errors found</p>")
                except BaseException as e:
                    r.append("<p>%s</p>" % repr(e))
                    v = False
                    r.append("<p>Errors found</p>")
                else:
                    if it['formated'] != for_result:
                        r.append("<h3>Wrong expected value</h3>")
                        r.append("<p>%s != %s</p>" % (it['formated'], for_result))
                        v = False
                    if it['valid'] != val_result:
                        r.append("<h3>Wrong expected validation</h3>")
                        r.append("<p>%s != %s</p>" % (it['valid'], val_result))
                        v = False
                    if v:
                        r.append("<p><b>Is Valid:</b>%s</p>" % ("True" if val_result else "False"))
                        r.append("<p><b>Normalized to:</b>%s</p>" % for_result)
                        r.append("<h3>Test end successfully</h3>")
                    else:
                        r.append("<h3 style='color: red'>Test end with errors</h3>")
                r.append('<hr/>')
            self.write(cr, uid, f['id'], { 'compile_message': '</br>'.join(r), 'tests_result': v, })
            return True

    def onchange_code(self, cr, uid, ids, validation, formating, message_ids, input_test_ids, context=None):
        """"""
        import pdb; pdb.set_trace()
        input_test_obj = self.pool.get('survey_methodology.input_test')
        for it in input_test_obj.browse(cr, uid, input_test_ids):
            import_text = it.input
            val_result = eval(validation, {'input': input_text, 'self': question_id})
            for_result = eval(formating, {'input': input_text, 'self': question_id})

        return {
            'test_result': True,
        }

format()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
