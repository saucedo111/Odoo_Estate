from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, exceptions


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
                                          default='south')
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")

    _sql_constraints = [('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be positive'),
                        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be positive'), ]

    @api.constrains('expected_price', 'selling_price')
    def _check_prices(self):
        for record in self:
            if record.selling_price == 0:
                continue
            if record.selling_price < 0.9 * record.expected_price:
                raise exceptions.ValidationError("The selling price must be greater than 90% of the expected price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else float(0)

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden_orientation != 'north' else ""

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("You cannot cancel a sold property")
            else:
                record.state = "canceled"

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise exceptions.UserError("You cannot sell a canceled property")
            else:
                record.state = "sold"
