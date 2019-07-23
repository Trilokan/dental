#

from odoo import models, fields


class Product(models.Model):
    _name = "arc.product"

    name = fields.Char(string="Product", required=True)
    product_uid = fields.Char(string="Code", required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

