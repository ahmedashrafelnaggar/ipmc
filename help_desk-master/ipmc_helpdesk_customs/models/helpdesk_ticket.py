from odoo import fields, models
from datetime import datetime, date


class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _description = "HelpdeskTicket"
    _inherit = "helpdesk.ticket"

    serial_number = fields.Char(string='Serial Number')
    transaction_date = fields.Date(string="Transaction Date")
    attachment_count = fields.Integer(
        string='Number of Attachments',
        store=True
    )
    transaction_type = fields.Selection(
        [('sale', 'Sale'), ('purchase', 'Purchase')],
        string='Transaction Type'
    )
    meeting = fields.Boolean(string='Meeting', defualt=True)
    meeting_datetime = fields.Datetime(string='Meeting Datetime')

