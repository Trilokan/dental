#

from odoo import models, fields


class Demo(models.Model):
    _name = "arc.demo"

    name = fields.Char(string="Name")
