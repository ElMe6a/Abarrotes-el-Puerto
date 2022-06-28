# -*- coding: utf-8 -*-
"""Res Partner"""
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Akshay Babu (Contact : odoo@cybrosys.com)
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
#    OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
################################################################################

from odoo import models, api, fields


class ResPartner(models.Model):
    """Overriding partner for setting credit and debit included in POS"""
    _inherit = 'res.partner'

    warning_stage = fields.Float(string='Warning Amount',
                                 compute='compute_active_limit',
                                 store=True, readonly=False,
                                 help="A warning message will appear once the "
                                      "selected customer is crossed warning "
                                      "amount. Set its value to 0.00 to disable"
                                      " this feature")
    blocking_stage = fields.Float(string='Blocking Amount',
                                  compute='compute_active_limit',
                                  readonly=False, store=True,
                                  help="Cannot make sales once the selected "
                                       "customer is crossed blocking amount."
                                       "Set its value to 0.00 to disable this "
                                       "feature")
    active_limit = fields.Boolean("Active Credit Limit",
                                  compute='compute_active_limit',
                                  readonly=False, store=True,
                                  default=False)

    @api.depends('parent_id.active_limit', 'parent_id.warning_stage',
                 'parent_id.blocking_stage')
    def compute_active_limit(self):
        for partner in self:
            if partner.parent_id:
                partner.active_limit = partner.parent_id.active_limit
                partner.warning_stage = partner.parent_id.warning_stage
                partner.blocking_stage = partner.parent_id.blocking_stage
            else:
                partner.active_limit = partner.active_limit
                partner.warning_stage = partner.warning_stage
                partner.blocking_stage = partner.blocking_stage

    @api.depends_context('force_company', 'pos_order_ids.state')
    def _credit_debit_get(self):
        super(ResPartner, self)._credit_debit_get()
        pos_orders = self.pos_order_ids.filtered(
            lambda x: x.partner_id and x.company_id == self.env.company and
                      x.paid_using_credit == True
        )
        for pos_order in pos_orders:
            credit_amount = pos_order.payment_ids.filtered_domain([('payment_method_id.name', '=', 'Credit')])
            amount_residue = 0
            for amount in credit_amount:
                amount_residue = amount_residue + amount.amount
            if amount_residue != 0:
                pos_order.partner_id.credit += amount_residue
