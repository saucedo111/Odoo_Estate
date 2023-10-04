from dateutil.relativedelta import relativedelta
from odoo import models, fields


class estate_Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Properties'

    name = fields.Char(required=True, default='My New House')
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'),
         ('canceled', 'Canceled')], default='new')
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=(fields.Date.today() + relativedelta(days=+90)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=4)
    living_area = fields.Integer(default=250)
    description = fields.Text(readonly=True, default='This is a beautiful house')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean(default=True)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
                                          default='north')
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
