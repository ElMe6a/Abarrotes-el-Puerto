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

from odoo import models, fields, api, _
from odoo.tools.translate import _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    warning_stage = fields.Float(string='Warning Amount',
                                 help="A warning message will appear once the selected customer is crossed warning amount."
                                      "Set its value to 0.00 to disable this feature")
    blocking_stage = fields.Float(string='Blocking Amount',
                                  help="Cannot make sales once the selected customer is crossed blocking amount."
                                       "Set its value to 0.00 to disable this feature")
    due_amount = fields.Float(string="Total Sale", compute="compute_due_amount")
    active_limit = fields.Boolean("Active Credit Limit", default=False)

    def compute_due_amount(self):
        for rec in self:
            if not rec.id:
                continue
            debit_amount = rec.debit
            credit_amount = rec.credit
            rec.due_amount = credit_amount - debit_amount

    @api.constrains('warning_stage', 'blocking_stage')
    def constrains_warning_stage(self):
        if self.active_limit:
            if self.warning_stage >= self.blocking_stage:
                if self.blocking_stage > 0:
                    raise UserError(_("Warning amount should be less than Blocking amount"))


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_due = fields.Boolean()
    is_warning = fields.Boolean()
    due_amount = fields.Float(related='partner_id.due_amount')

    def action_confirm(self):
        """To check the selected customers due amount is exceed than blocking stage"""
        if self.partner_id.active_limit:
            if self.due_amount >= self.partner_id.blocking_stage:
                if self.partner_id.blocking_stage != 0:
                    
                    raise UserError(_("This customer is in  Blocking Stage and has %s to pay") % self.due_amount)
        return super(SaleOrder, self).action_confirm()

    @api.onchange('partner_id')
    def check_due(self):
        """To show the due amount and warning stage"""
        if self.partner_id and self.partner_id.due_amount > 0:
            self.has_due = True
        else:
            self.has_due = False
        if self.partner_id and self.partner_id.active_limit:
            if self.due_amount >= self.partner_id.warning_stage:
                if self.partner_id.warning_stage != 0:
                    self.is_warning = True
        else:
            self.is_warning = False



