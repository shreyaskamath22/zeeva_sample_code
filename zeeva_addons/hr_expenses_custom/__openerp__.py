# -*- encoding: utf-8 -*-
##############################################################################
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

{
    'name': 'Employee Expenses ',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """

Employee Expenses In Human Resources 
========================

    """,
    'author': 'ujwala pawade',
    'website': 'http://www.zeeva.com',
    'license': 'AGPL-3',
    'depends': ['hr', 'hr_expense', ],
    'data': [
        'hr_view.xml',
        'hr_expense_sequence.xml',
        'hr_expense_custom_data.xml',
        'reports.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'images': [],
    'css': ['static/src/css/expense_custom.css'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
