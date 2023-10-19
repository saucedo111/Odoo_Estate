from odoo import models, fields, api


class estate_property_type(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _order = 'name'

    name = fields.Char(required=True, default='House')
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer('Sequence')
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer('Offer Count', compute='_compute_offer_count')

    _sql_constraints = [('check_name', 'UNIQUE (name)', 'The name must be unique')]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
