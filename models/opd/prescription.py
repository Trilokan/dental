#

from odoo import models, fields

CONSUMPTION_TYPE = [("before_food", "Before Food"), ("after_food", "After Food")]


class Prescription(models.Model):
    _name = "arc.prescription"

    product_id = fields.Many2one(comodel_name="arc.product", string="Medicine")
    morning = fields.Boolean(string="Morning")
    noon = fields.Boolean(string="Noon")
    evening = fields.Boolean(string="Evening")
    consumption_type = fields.Selection(selection=CONSUMPTION_TYPE, string="Consumption")
    quantity = fields.Integer(string="Quantity", default=0)
    treatment_id = fields.Many2one(comodel_name="dental.treatment", string="Treatment")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
