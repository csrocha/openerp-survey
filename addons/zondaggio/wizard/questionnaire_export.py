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
from openerp import netsvc
from openerp.osv import osv, fields
from openerp.tools.translate import _

import logging
import csv
import StringIO, cStringIO, codecs
import base64
import hashlib

_logger = logging.getLogger(__name__)

class UnicodeDictWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
        self.fieldnames = self.writer.fieldnames

    def writerow(self, row):
        self.writer.writerow(dict([(k.encode("utf-8"), v and v.encode("utf-8") or v) for k,v in row.items()]))
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def list_inputs(cur, survey_id):
        _q_input = """
                select QA.name, Q.variable_name, valid, input, message, formated
                        from sondaggio_answer as A 
                        left join sondaggio_node as Q on (A.question_id = Q.id) 
                        left join sondaggio_questionnaire as QA on (A.questionnaire_id = QA.id) 
                        where Q.type = 'Variable'
                            and QA.survey_id = %s
                        order by QA.name, Q.variable_name;
                """ % survey_id
        cur.execute(_q_input)
        for i in cur.fetchall():
                yield i

def list_variables(cur):
        _q_variables = """
                select variable_name from sondaggio_node where type = 'Variable' and variable_name != '' order by complete_place;
        """
        cur.execute(_q_variables)
        return [ i[0] for i in cur.fetchall() ]

def iter_dump(iterator, out_csv, keys):
        out_csv.writerow((lambda x: dict(zip(x,x)))(out_csv.fieldnames))

        row = None
        questionaire = None

        for i in iterator:
                if questionaire !=  i[0]:
                        questionaire = i[0]
                        if row is not None:
                                out_csv.writerow(row)
                        row = dict( (k,None) for k in keys )
                        row['questionaire'] = questionaire
                row[i[1]] = i[3] #i[2:]
        out_csv.writerow(row)
 
def dump_inputs(cur, survey_id):
        keys = [u'questionaire'] + list_variables(cur)

        out_file = StringIO.StringIO()
        out_csv = UnicodeDictWriter(out_file, fieldnames=keys)

        iter_dump(list_inputs(cur, survey_id), out_csv, keys)

        return out_file

class questionnaire_export(osv.osv_memory):
    """"""
    
    _name = 'sondaggio.questionnaire_export'

    _columns = {
        'survey_id': fields.many2one('sondaggio.survey', string='Survey'),
        'data': fields.binary('File', readonly=True),
        'state': fields.selection( [ ('choose','choose'), ('get', 'get') ] ),
        'name': fields.char( "Filename", size=16, readonly=True ),
    }

    _defaults = {
        'state': 'choose',
    }

    def create_report(self, cr, uid, ids, context=None):
        """"""
        this = self.browse(cr, uid, ids)[0]
        output = dump_inputs(cr, this.survey_id.id)
        out = base64.encodestring(output.getvalue())
        self.write(cr, uid, ids, {
            'state': 'get',
            'data': out,
            'name': 'questionnaires.csv'},
            context=context)
        return {
            'name': _('Export Questionnaires'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'sondaggio.questionnaire_export',
            'domain': [],
            'context': dict(context, active_ids=ids),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': ids and ids[0] or False,
        }

questionnaire_export()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
