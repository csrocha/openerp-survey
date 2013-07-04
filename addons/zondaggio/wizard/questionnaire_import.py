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

_logger = logging.getLogger(__name__)

class questionnaire_import(osv.osv_memory):
    """"""
    
    _name = 'sondaggio.questionnaire_import'
    _inherit = [ _name ]

    def take_names(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError

    def do_load_file(self, cr, uid, ids, context=None):
        """"""
        # Fill list of columns.
        obj_import_file_column = self.pool.get('sondaggio.import_file_column')
        for w in self.browse(cr, uid, ids, context=context):
            # Unlik columns if exists
            #ifc_ids = [ i.id for i in w.import_file_column_ids ]
            ifc_ids = obj_import_file_column.search(cr, uid, [])
            obj_import_file_column.unlink(cr, uid, ifc_ids)
            # Create columns from file
            data = StringIO.StringIO(base64.b64decode(w.in_file))
            rows = csv.reader(data)
            header = rows.next()
            print header
            for k in header:
                obj_import_file_column.create(cr, uid, { 'name': k, 'questionnaire_import_id': w.id })

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
        for w in self.browse(cr, uid, ids, context=context):
            data = StringIO.StringIO(base64.b64decode(w.in_file))
        #for qi in self.browse(cr, uid, ids, context=context):
        #    self._import_binary(cr, uid, ids, binary=qi.in_file, survey_id=qi.survey_id, column_name=qi.name_field)

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

    def _import_binary(self,cr,uid,ids,binary="",survey_id=None,column_name=None):
        data = StringIO.StringIO(base64.b64decode(binary))
        rows = csv.reader(data)
        cantidad = 0
        dict_values = {}
        cabecera = []
        for row in rows:
            cadena = str(row).split('\\t')
            cadena[0] = cadena[0].replace("['","")
            cadena[len(cadena)-1] = cadena[len(cadena)-1].replace("']","")
            if cantidad == 0:
                for value_cadena in cadena:
                    dict_values[value_cadena] = []
                    cabecera.append(value_cadena)
            else:
                for index in range(len(cadena)):
                    indice = cabecera[index]
                    dict_values[indice].append(cadena[index])
            cantidad = cantidad + 1
            # creates questionaires
        questionnaire_obj = self.pool.get('sondaggio.questionnaire')
        parameter_obj = self.pool.get('sondaggio.parameter')
        index = 0
        for nombre in dict_values[column_name]:
            vals_questionnaire = {'name': nombre, 'survey_id': survey_id}
            questionnaire_id = questionnaire_obj.create(cr,uid,vals_questionnaire)
            _logger.debug(str(questionnaire_id))    
            index = index+1
            for key in dict_values.keys():
                if key <> column_name:
                    try:
                        vals_parameter = {'name': key,
                                'questionnaire_id': questionnaire_id,
                                'value': dict_values[key][index]}
                        parameter_id = parameter_obj.create(cr,uid,vals_parameter)
                        _logger.debug(str(parameter_id))
                    except:
                        pass

    def _import_parameter_filename(self,cr,uid,ids=None,context=None):
        sondaggio_ids = self.search(cr,uid,[('id','>',0)])
        dict_sondaggio = {}
        for sondaggio in sondaggio_obj.browse(cr,uid,sondaggio_ids):
            self._import_filename(cr,uid,ids,sondaggio.filename,sondaggio.survey_id.id,sondaggio.column_name)
            _logger.debug(sondaggio.filename)

    def load_file(self, cr, uid, ids=None, context=None):
        import pdb; pdb.set_trace()
        return True

questionnaire_import()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
