from odoo import api, fields, models, _, SUPERUSER_ID, tools
import logging
from . import api_global_function

_logger = logging.getLogger(__name__)
DATES_FORMAT = "%Y-%m-%d"
class hr_applicant(models.Model):
    _inherit = "hr.applicant"

    def check_applicant_vals(self, args):
        applicant_vals = {'active': True}
        if args.get("RequestID", False):
            applicant_vals.update({'id': args.get("RequestID", False)})
        try:
            if not args.get('partner_name', False):
                return False, api_global_function.return_failed_request_vals("Customer Name Not provided",
                                                                             "عفوا العميل مش موجود")
            applicant_vals.update({'name': args.get("partner_name", False),'partner_name': args.get("partner_name", False)})
            if not args.get('iqama_number', False):
                return False, api_global_function.return_failed_request_vals("Iqama Number Not provided",
                                                                             "عفوا رقم الهويه مش موجود")
            applicant_vals.update({'iqama_number': args.get("iqama_number", False)})

            if not args.get('iqama_exp_date', False):
                return False, api_global_function.return_failed_request_vals("Iqama Expiry Date Not provided",
                                                                             "عفوا تاريخ انتهاء الاقامه مش موجود")
            applicant_vals.update({'iqama_exp_date': args.get("iqama_exp_date", False)})
            if not args.get('iqama_src_id', False):
                return False, api_global_function.return_failed_request_vals(
                    "Residential Source Not Provided",
                    "عفوا مصدر الاقامه غير موجود ")
            if not self.env['res.country.state'].sudo().search([('id', '=', args.get('iqama_src_id', False))]):
                return False, api_global_function.return_failed_request_vals("Residential Source Not Correct",
                                                                             "عفوا مصدر الاقامة غير صحيح")
            applicant_vals['iqama_src_id'] = args.get('iqama_src_id', False)

            if not args.get('nationality_id', False):
                return False, api_global_function.return_failed_request_vals(
                    "Nationality Not Provided",
                    "عفوا الجنسية غير موجود ")
            if not self.env['res.country'].sudo().search([('id', '=', args.get('nationality_id', False))]):
                return False, api_global_function.return_failed_request_vals("Nationality Not Correct",
                                                                             "عفوا الجنسية غير صحيح")
            applicant_vals['nationality_id'] = args.get('nationality_id', False)

            if not args.get('gender', False):
                return False, api_global_function.return_failed_request_vals(
                    "Gender Not Provided",
                    "عفوا النوع غير موجود ")
            if args.get('gender', False) not in ['male','female']:
                return False, api_global_function.return_failed_request_vals("Gender Not Correct",
                                                                             "عفوا النوع غير صحيح")
            applicant_vals['gender'] = args.get('gender', False)
        except Exception as e:
            arabic_message = "%s  " % _(str(e)),
            englishmessage = "%s." % _(str(e))
            return False, api_global_function.return_failed_request_vals(englishmessage, arabic_message)
        return True, applicant_vals

        # applicant_vals['speciality'] = args.get('speciality', False)
        # if not args.get('speciality', False):
        #     return False, api_global_function.return_failed_request_vals(
        #         "Speciality Not Provided",
        #         "عفوا الجنسية غير موجود ")

        applicant_vals['speciality'] = args.get('speciality', False)
        if not args.get('speciality', False):
            return False, api_global_function.return_failed_request_vals("speciality  Not provided",
                                                                         "عفوا العميل مش موجود")


        


    def add_update_hr_applicant(self, **args):
        request_id = args.get("RequestID", False)
        check_vals, applicant_vals = self.check_applicant_vals(args)
        if not check_vals:
            return applicant_vals
        try:
            if not request_id:
                hr_applicant_obj = self.with_user(args.get('userId')).sudo().create(applicant_vals)
            else:
                #Update Request ID
                hr_applicant_obj = self.with_user(args.get('userId')).sudo().browse(request_id)
                hr_applicant_obj.with_user(args.get('userId')).sudo().write(applicant_vals)
        except Exception as e:
            self.env.cr.rollback()
            return api_global_function.return_failed_api(_(str(e)))
        if not request_id:
            return api_global_function.return_success_creation_api(hr_applicant_obj.id, hr_applicant_obj.id)
        else:
            return api_global_function.return_success_update_api(hr_applicant_obj.id, hr_applicant_obj.id)

