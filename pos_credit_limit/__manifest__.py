# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Abhishek E T (Contact : odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0
#    (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the
#    Software or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
#    USE OR OTHER DEALINGS IN THE SOFTWARE.
#
################################################################################
{
    'name': 'POS Credit Limit',
    'version': '15.0.1.0.1',
    'summary': """
    To provide credits for regular customers in POS
    """,
    'description': """
        To provide credits for regular customers in POS.
        This app works with the Customer Credit Limit with Due Amount Warning
        App.
        You can set a warning stage and blocking stage for the credit to a 
        particular company.
        This module also shows the due amount of each customer.
    """,
    'category': 'Point of Sale',
    'author': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['account', 'point_of_sale', 'sales_credit_limit'],
    'data': [
        'data/data.xml',
        'views/pos_order.xml',
        'views/account_journal_views.xml',
    ],
    'assets': {
        'point_of_sale.pos_assets_backend': [
            'pos_credit_limit/static/src/js/credit.js',
        ],
        'web.assets_qweb': [
          'pos_credit_limit/static/src/xml/*.xml',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'price': 9,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': False,
}
