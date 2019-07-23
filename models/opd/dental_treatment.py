#

from odoo import models, fields, api
from datetime import datetime
import pdfkit
import base64
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition


current_date = datetime.now().strftime("%Y-%m-%d")


class DentalTreatment(models.Model):
    _name = "dental.treatment"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient", required=True)
    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Doctor", required=True)
    symptoms_ids = fields.Many2many(comodel_name="arc.symptoms", string="Symptoms")
    diagnosis_ids = fields.Many2many(comodel_name="arc.diagnosis", string="Diagnosis")
    diagnosis_comment = fields.Text(string="Comment")
    treatment_ids = fields.Many2many(comodel_name="arc.treatment", string="Treatment")
    treatment_comment = fields.Text(string="Comment")
    teeth_ids = fields.One2many(comodel_name="arc.teeth", inverse_name="treatment_id", string="Teeth")
    prescription_ids = fields.One2many(comodel_name="arc.prescription", inverse_name="treatment_id", string="Prescription")
    report = fields.Html(string="Report")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    file_name = fields.Char(string="File Name", default="treatment.pdf")
    treatment_pdf = fields.Binary(string="Treatment PDF")
    prescription_pdf = fields.Binary(string="Prescription PDF")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    comment = fields.Text(string="Comment")

    def get_comma(self, recs):
        record = ""
        for rec in recs:
            if record == "":
                record = "{1}".format(record, rec.name)
            else:
                record = "{0}, {1}".format(record, rec.name)

        return record

    @api.multi
    def get_prescription_table(self):
        record_id = self.env["arc.template"].search([("template_uid", "=", "PRESCRIPTION TABLE")])

        data_table = ""

        for rec in self.prescription_ids:
            morning = "Y" if rec.morning else "-"
            noon = "Y" if rec.noon else "-"
            evening = "Y" if rec.evening else "-"
            consumption_type = rec.consumption_type.title().replace("_", " ")
            data_table = """{0}<tr><td>{1}</td>"
                                            <td>{2}</td>
                                            <td>{3}</td>
                                            <td>{4}</td>
                                            <td>{5}</td>
                                            <td>{6}</td></tr>""".format(data_table,
                                                                        rec.product_id.name,
                                                                        morning,
                                                                        noon,
                                                                        evening,
                                                                        consumption_type,
                                                                        rec.quantity)

        data_dict = {"data_table": data_table}
        html_data = record_id.template.format(**data_dict)

        return html_data

    @api.multi
    def trigger_report(self):
        symptoms = self.get_comma(self.symptoms_ids)
        diagnosis = self.get_comma(self.diagnosis_ids)
        treatment = self.get_comma(self.treatment_ids)
        diagnosis_comment = self.diagnosis_comment or ""
        treatment_comment = self.treatment_comment or ""

        prescription_data = self.get_prescription_table()

        data_dict = {"company_logo": "data:image/png;base64,{0}".format(self.company_id.logo),
                     "company_name": self.company_id.name if self.company_id.name else "",
                     "company_address": self.company_id.address if self.company_id.address else "",
                     "doctor_name": self.doctor_id.person_id.name if self.doctor_id.person_id.name else "",
                     "patient_name": self.patient_id.person_id.name if self.patient_id.person_id.name else "",
                     "patient_id": self.patient_id.person_id.person_uid if self.patient_id.person_id.person_uid else "",
                     "patient_address": "",
                     "info_no": self.name if self.name else "",
                     "info_date": self.date if self.date else "",
                     "symptoms": symptoms if symptoms else "",
                     "diagnosis": diagnosis if diagnosis else "",
                     "treatment": treatment if treatment else "",
                     "diagnosis_comment": diagnosis_comment if diagnosis_comment else "",
                     "treatment_comment": treatment_comment if treatment_comment else "",
                     "prescription_data": prescription_data}

        record_id = self.env["arc.template"].search([("template_uid", "=", "OPD")])

        html_data = record_id.template.format(**data_dict)
        css = "/opt/dental/static/src/css/template.css"
        pdfkit.from_string(html_data, '/opt/kon/out.pdf', css=css)
        pdf_file = open('/opt/kon/out.pdf', 'rb')
        pdf_data = pdf_file.read()
        pdf_file.close()
        out = base64.b64encode(pdf_data)

        self.write({'treatment_pdf': out, 'file_name': 'Treatment.pdf'})

        return {
            'type': 'ir.actions.act_url',
            'url': '/dental/treatment?model=dental.treatment&id=%s' % (self.id),
            'target': 'new',
        }

    @api.multi
    def trigger_prescription(self):
        record_id = self.env["arc.template"].search([("template_uid", "=", "PRESCRIPTION")])

        data_table = ""

        for rec in self.prescription_ids:
            morning = "Y" if rec.morning else "-"
            noon = "Y" if rec.noon else "-"
            evening = "Y" if rec.evening else "-"
            consumption_type = rec.consumption_type.title().replace("_", " ")
            data_table = """{0}<tr><td>{1}</td>"
                                    <td>{2}</td>
                                    <td>{3}</td>
                                    <td>{4}</td>
                                    <td>{5}</td>
                                    <td>{6}</td></tr>""".format(data_table,
                                                                rec.product_id.name,
                                                                morning,
                                                                noon,
                                                                evening,
                                                                consumption_type,
                                                                rec.quantity)

        data_dict = {"company_logo": "data:image/png;base64,{0}".format(self.company_id.logo),
                     "company_name": self.company_id.name if self.company_id.name else "",
                     "company_address": self.company_id.address if self.company_id.address else "",
                     "patient_name": self.patient_id.person_id.name if self.patient_id.person_id.name else "",
                     "patient_id": self.patient_id.person_id.person_uid if self.patient_id.person_id.person_uid else "",
                     "patient_address": "",
                     "info_no": self.name if self.name else "",
                     "info_date": self.date if self.date else "",
                     "data_table": data_table}

        html_data = record_id.template.format(**data_dict)
        css = "/opt/dental/static/src/css/template.css"
        pdfkit.from_string(html_data, '/opt/kon/out.pdf', css=css)
        pdf_file = open('/opt/kon/out.pdf', 'rb')
        pdf_data = pdf_file.read()
        pdf_file.close()
        out = base64.b64encode(pdf_data)

        self.write({'prescription_pdf': out, 'file_name': 'prescription.pdf'})

        return {
            'type': 'ir.actions.act_url',
            'url': '/dental/prescription?model=dental.treatment&id=%s' % (self.id),
            'target': 'new',
        }

    @api.multi
    def trigger_register_payment(self):

        return {
            'name': ('Register Payment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'arc.payment',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_person_id': self.patient_id.person_id.id,
                        'default_ref': self.name}
        }

    @api.multi
    def trigger_treatment_history(self):

        return {
            'name': ('Treatment History'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'dental.treatment',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': [('patient_id', '=', self.patient_id.id)]
        }

    @api.multi
    def trigger_next_appointment(self):

        return {
            'name': ('Next Appointment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'arc.appointment',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_doctor_id': self.patient_id.id,
                        'default_appointment_for': self.patient_id.id}
        }

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(DentalTreatment, self).create(vals)


class OPDPDF(http.Controller):
    _cp_path = '/dental'

    @http.route('/dental/treatment', type='http', auth="public")
    def treatment_pdf_download(self, **data):
        record_id = http.request.env['dental.treatment'].search([('id', '=', data.get('id'))])
        if record_id:
            filecontent = base64.b64decode(record_id.treatment_pdf)
            filename = record_id.file_name
            if filecontent and filename:
                return request.make_response(filecontent,
                                             headers=[('Content-Type', 'application/pdf'),
                                                      ('Content-Disposition', content_disposition(filename))])
        return request.not_found()

    @http.route('/dental/prescription', type='http', auth="public")
    def prescription_pdf_download(self, **data):
        record_id = http.request.env['dental.treatment'].search([('id', '=', data.get('id'))])
        if record_id:
            filecontent = base64.b64decode(record_id.prescription_pdf)
            filename = record_id.file_name
            if filecontent and filename:
                return request.make_response(filecontent,
                                             headers=[('Content-Type', 'application/pdf'),
                                                      ('Content-Disposition', content_disposition(filename))])
        return request.not_found()
