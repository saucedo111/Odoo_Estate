from datetime import date

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, exceptions


class estate_property_offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    create_date = fields.Date(default=fields.Date.today())
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _sql_constraints = [('check_price', 'CHECK(price > 0)', 'The price must be positive')]

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
        if self.property_id.state != 'offer_accepted':
            self.property_id.state = 'offer_accepted'
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price

    @api.model
    def create(self, vals):
        self.env['estate.property'].browse(vals['property_id']).receive()
        return super().create(vals)
