# -*- coding: utf-8 -*-
"""Pos order"""
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
#    Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#    OTHERWISE,ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
#    USE OR OTHER DEALINGS IN THE SOFTWARE.
#
################################################################################

from odoo import models, fields


class PosOrder(models.Model):
    """Breaking the creation of credit payment journal"""
    _inherit = 'pos.order'

    paid_using_credit = fields.Boolean(string='Paid Using Credit', compute='_compute_paid_using_credit')

    def _compute_paid_using_credit(self):
        for rec in self:
            pay_methods = rec.payment_ids.mapped('payment_method_id')
            rec.paid_using_credit = False
            if pay_methods:
                if pay_methods[0].name == 'Credit':
                    rec.paid_using_credit = True

    def add_payment(self, data):
        """Create a new payment for the order"""
        self.ensure_one()
        payment_method = self.env['pos.payment.method'].search([
            ('id', '=', data['payment_method_id'])])
        if not payment_method.journal_id.pos_credit or payment_method.journal_id.id == self.env.ref('pos_credit_limit.credit_journal').id:
            self.env['pos.payment'].create(data)
            self.amount_paid = sum(self.payment_ids.mapped('amount'))
