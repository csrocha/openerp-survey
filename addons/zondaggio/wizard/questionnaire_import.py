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
import StringIO
import base64
import hashlib

_logger = logging.getLogger(__name__)

class questionnaire_import(osv.osv_memory):
    """"""
    
    _name = 'sondaggio.questionnaire_import'
    _inherit = [ _name ]

    _columns = {
        'version_column_id': fields.many2one('sondaggio.import_file_column', string='Version column'),
    }

    def do_load_file(self, cr, uid, ids, context=None):
        """"""
        # Fill list of columns.
        obj_import_file_column = self.pool.get('sondaggio.import_file_column')
        for w in self.browse(cr, uid, ids, context=context):
            # Unlink columns if exists
            w.write({ 'import_file_column_ids': [ (5,) ] })
            # Remove all because before sentence don't look works.
            ifc_ids = obj_import_file_column.search(cr, uid, [])
            obj_import_file_column.unlink(cr, uid, ifc_ids)
            # Create columns from file
            data = StringIO.StringIO(base64.b64decode(w.in_file))
            rows = csv.reader(data)
            header = rows.next()
            w.write({ 'import_file_column_ids': [ (0, 0, dict(name=k)) for k in header ] })

        self.write(cr, uid, ids, {'state': 'config'}, context=context)
        return {
            'name': _('Import Questionnaire'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'sondaggio.questionnaire_import',
            'domain': [],
            'context': dict(context, active_ids=ids),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': ids and ids[0] or False,
        }

    def do_import(self, cr, uid, ids, context=None):
        """"""
        _logger.info('Importing questionnaires.')

        questionnaire_obj = self.pool.get('sondaggio.questionnaire')
        parameter_obj = self.pool.get('sondaggio.parameter')

        c = 0
        u = 0
        for w in self.browse(cr, uid, ids, context=context):
            data = StringIO.StringIO(base64.b64decode(w.in_file))
            rows = csv.reader(data)
            fields = rows.next()
            column_name = w.selected_column_id.name
            column_version = w.version_column_id.name
            survey_id = w.survey_id.id
            crc = None
            for r in rows:
                rdict = dict(zip(fields, r))
                questionnaire_ids = questionnaire_obj.search(cr, uid, [('name','=',rdict[column_name])])
                if questionnaire_ids:
                    q = questionnaire_obj.browse(cr, uid, questionnaire_ids)[0]
                    parameters = { p.name: p.value for p in q.parameter_ids }
                    if int(parameters.get(column_version, 0)) < int(rdict[column_version]):
                        dwrite = {
                            'parameter_ids': [ (0,0,{ 'name': k.lower(), 'value': v }) for k, v in rdict.items() if k != column_name ],
                        }
                        questionnaire_obj.write(cr, uid, [q.id], dwrite)
                        if not(u % 40): _logger.info('Updating %i questionnaires and continue.' % u+1)
                        u = u +1
                else:
                    m = hashlib.md5()
                    m.update(rdict[column_name])
                    dwrite = {
                        'name': rdict[column_name],
                        'code': m.hexdigest(),
                        'survey_id': survey_id,
                        'parameter_ids': [ (0,0,{ 'name': k, 'value': v }) for k, v in rdict.items() if k != column_name ],
                    }
                    questionnaire_obj.create(cr, uid, dwrite)
                    if not(c % 40): _logger.info('Created %i questionnaires and continue.' % c+1)
                    c = c + 1

        _logger.info('Created %i questionnaires.' % c)
        _logger.info('Updated %i questionnaires.' % u)

        self.write(cr, uid, ids, {'state': 'done'}, context=context)
        return {
            'name': _('Import Questionnaire'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'sondaggio.questionnaire_import',
            'domain': [],
            'context': dict(context, active_ids=ids),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': ids and ids[0] or False,
        }

    def do_continue(self, cr, uid, ids, context=None):
        """"""
        for w in self.browse(cr, uid, ids, context=context):
            survey_id = w.survey_id.id

        return {
            'name': _('Questionnaires'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'res_model': 'sondaggio.questionnaire',
            'domain': [('survey_id','=',survey_id)],
            'context': context,
            'type': 'ir.actions.act_window',
            'target': False,
            'res_id': False,
        }

questionnaire_import()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
