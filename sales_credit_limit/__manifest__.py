# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Mashood K.U (Contact : odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################

{
    'name': 'Customer Credit Limit with Due Amount Warning',
    'version': '15.0.1.0.0',
    'summary': 'An advanced way to handle customer credit limit through warning and blocking stage.',
    'description': """This module helps you to handle customer credit limit in an efficient way.
                You can set a warning stage and blocking stage to a particular customer.
                This module also shows the due amount of a customer while creating an order.""",
    'category': 'Sales',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'live_test_url': 'https://www.youtube.com/watch?v=aE56em5LsY4',
    'depends': ['base', 'sale'],
    'website': 'https://www.cybrosys.com',
    'data': [
        'views/credit_limit_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'price': 20,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': False,
}
