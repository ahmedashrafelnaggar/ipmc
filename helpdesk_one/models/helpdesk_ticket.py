from odoo import fields, models, api,_
from datetime import datetime, date


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    serial_number = fields.Char(string='Serial Number', default=lambda self:_('New'))
    transaction_date = fields.Date(string="Transaction Date")
    attachment_count = fields.Integer(string='Number of Attachments')
    meeting = fields.Boolean(string='Meeting')
    meeting_datetime = fields.Datetime(string='Meeting Datetime')
    oolweh_mualamah_priority = fields.Selection([
        ('عاجل', 'عاجل'),
        ('عاجل جدا وهام', 'عاجل جدا وهام'),
        ('عاجل جدا وهام يسلم حالا', 'عاجل جدا وهام يسلم حالا'),
        ('سري', 'سري'),
        ('سري-عاجل جدا وهام', 'سري-عاجل جدا وهام')
    ], string='اولويه المعامله')

    transaction_action = fields.Selection(
        [
            ('complete_requirements', 'اكمال اللازم'),
            ('study_preparation', 'الدراسه واعداد اللازم'),
            ('utilize_available_information', 'للافاده بما لديكم'),
            ('provide_feedback', 'لابداء المرئيات'),
            ('approve_execution', 'لاعتماد انفاذ موجبه'),
            ('preserve', 'تحفظ'),
            ('for_consultation', 'للمفاهمة'),
            ('for_review_and_notification', 'للاطلاع والاحاطه'),
            ('for_circulation', 'للتعميم'),
            ('attachment_to_previous', 'الحاقا للسابقه'),
            ('no_objection', 'لامانع'),
            ('for_follow_up', 'للمتابعه')
        ],
        string='اجراء المعامله'
    )
    # ticket_number = fields.Char(string='Transaction Number')
    # ticket_type = fields.Selection(string='Transaction Type')

    @api.model_create_multi
    def create(self, vals):
        rec = super(HelpdeskTicket, self).create(vals)
        if rec.serial_number == _('New'):
            rec.serial_number = self.env['ir.sequence'].next_by_code('helpdesk.ticket_seq')
        return rec




