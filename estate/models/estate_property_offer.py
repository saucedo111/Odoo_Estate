from datetime import date

from dateutil.relativedelta import relativedelta
from odoo.tools import date_utils
from odoo import models, fields, api


class estate_property_offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], default='accepted', copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    create_date = fields.Date(default=fields.Date.today())

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    record.validity = (record.date_deadline - record.create_date).days
                else:
                    record.validity = (record.date_deadline - date.today()).days

    def action_refuse(self):
        for record in self:
            record.status = 'refused'

    def action_accept(self):
        for record in self:
            record.status = 'accepted'



