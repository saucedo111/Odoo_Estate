from odoo import models


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        res = super().action_sold()
        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        for prop in self:
            self.env['account.move'].create(
                {'partner_id': prop.buyer_id.id, 'move_type': 'out_invoice', 'journal_id': journal.id})

        return res
