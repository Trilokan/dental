#

from odoo import models, fields

TEETH = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
         (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16),
         (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24),
         (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32)]

TEETH_TYPE = [("incisor", "Incisor"), ("canine", "Canine"), ("pre_molar", "Pre Molar"), ("molar", "Molar")]


class Teeth(models.Model):
    _name = "arc.teeth"

    teeth = fields.Selection(selection=TEETH, string="Teeth")
    teeth_type = fields.Selection(selection=TEETH_TYPE, string="Teeth Type")
    treatment_ids = fields.Many2one(comodel_name="arc.treatment", string="Treatment")
    treatment_id = fields.Many2one(comodel_name="dental.treatment", string="Treatment")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
