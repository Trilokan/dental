# -*- coding: utf-8 -GPK*-

{
    "name": "Dental",
    "version": "1.0",
    "author": "La Mars",
    "website": "http://",
    "category": "Dental",
    "sequence": 1,
    "summary": "Hospital Management System",
    "description": """

    Hospital Management System

    Patient Management
    Employee Management
    Purchase Management
    Pharmacy Management
    Assert Management
    Accounts Management

    """,
    "depends": ["base", "mail", "auth_signup"],
    "data": [

        "views/assert_backend.xml",

        "security/security.xml",
        "security/base.xml",
        "security/billing.xml",
        "security/configuration.xml",
        "security/general.xml",
        "security/opd.xml",
        "security/staff.xml",
        "security/ir.model.access.csv",

        "sequence/base.xml",
        "sequence/testing.xml",

        # Base
        "views/base/patient.xml",
        "views/base/staff.xml",
        "views/base/person.xml",

        # Contact
        "views/contact/contact.xml",
        "views/contact/patient.xml",
        "views/contact/staff.xml",
        "views/contact/supplier.xml",
        "views/contact/service.xml",

        # General
        "views/general/hr_category.xml",

        # Reception
        "views/reception/doctor_availability.xml",
        "views/reception/doctor_timings.xml",
        "views/reception/notes.xml",
        "views/reception/reminder.xml",

        # OPD
        "views/opd/appointment.xml",
        "views/opd/dental_treatment.xml",
        "views/opd/prescription.xml",
        "views/opd/clinical_notes.xml",

        # Billing
        "views/billing/order.xml",
        "views/billing/patient_invoice.xml",
        "views/billing/payment.xml",
        "views/billing/tax.xml",

        # Demo
        "views/demo/braces.xml",
        "views/demo/crown.xml",
        "views/demo/dental_fillings.xml",
        "views/demo/dental_implant.xml",
        "views/demo/root_canal_treatment.xml",

        # Configuration
        "views/configuration/appointment_reason.xml",
        "views/configuration/appointment_type.xml",
        "views/configuration/symptoms.xml",
        "views/configuration/diagnosis.xml",
        "views/configuration/treatment.xml",
        "views/configuration/invoice_description.xml",

        # Menu
        "views/menu/menu.xml",

        "data/prescrip_template.xml",
        "data/prescrip_table_template.xml",
        "data/treatment_template.xml",
        "data/opd_template.xml",


    ],
    "demo": [

    ],
    "qweb": [

    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}