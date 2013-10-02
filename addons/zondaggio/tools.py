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

def local_dict(input_text, question=None):
        r = {
            'input': input_text or '',
            'linput': input_text and input_text.lower() or '',
            'uinput': input_text and input_text.upper() or '',
            'sinput': input_text and input_text.strip() or '',
            'slinput': input_text and input_text.strip().lower() or '',
            'suinput': input_text and input_text.strip().upper() or '',
            'inrange': lambda v, _min=None, _max=None: _min <= v and v < _max,
            'self': question,
            're': re,
            'match': lambda regexp, _input: _input and re.match(regexp, _input.strip()) is not None,
            'imatch': lambda regexp, _input: _input and re.match(regexp, _input.strip(), re.I) is not None,
            'sub': lambda regexp, replace, _input: _input and re.match(regexp, _input.strip()) and re.sub(regexp, replace, _input.strip()),
            'isub': lambda regexp, replace, _input: _input and re.match(regexp, _input.strip()) and re.sub(regexp, replace, _input.strip(), re.I),
        }
        return r

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
