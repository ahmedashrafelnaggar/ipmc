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
            if not self.env['res.country'].sudo().search([('ex_id', '=', args.get('nationality_id', False))]):
                return False, api_global_function.return_failed_request_vals("Nationality Not Correct",
                                                                             "عفوا الجنسية غير صحيح")
            applicant_vals['nationality_id'] = args.get('nationality_id', False)

            # this is selection
            if not args.get('gender', False):
                return False, api_global_function.return_failed_request_vals(
                    "Gender Not Provided",
                    "عفوا النوع غير موجود ")
            if args.get('gender', False) not in ['male','female']:
                return False, api_global_function.return_failed_request_vals("Gender Not Correct",
                                                                             "عفوا النوع غير صحيح")
            applicant_vals['gender'] = args.get('gender', False)

            if not args.get('speciality', False):
                return False, api_global_function.return_failed_request_vals("speciality Not Provided",
                                                                             "عفوا التخصص غير موجود ")
            applicant_vals.update({'speciality': args.get("speciality", False)})

            if not args.get('birth_date', False):
                return False, api_global_function.return_failed_request_vals("Birth Date Not provided",
                                                                                     "عفوا تاريخ الميلاد مش موجود")
            applicant_vals.update({'birth_date': args.get("birth_date", False)})

            if not args.get('address', False):
                return False, api_global_function.return_failed_request_vals("Address Not provided",
                                                                                     "عفوا العنوان مش موجود")
            applicant_vals.update({'address': args.get("address", False)})

            if not args.get('Employement_Status', False):
                return False, api_global_function.return_failed_request_vals(
                    "Employement Status Not Provided",
                    "عفوا الحالة الوظيفية غير موجود ")
            if not self.env['employment.status'].sudo().search([('id', '=', args.get('Employement_Status', False))]):
                return False, api_global_function.return_failed_request_vals("Employement Status Not Correct",
                                                                             "عفوا الحالة الوظيفية غير صحيح")
            applicant_vals['Employement_Status'] = args.get('Employement_Status', False)

            if not args.get('employer', False):
                return False, api_global_function.return_failed_request_vals(" Employer Not provided",
                                                                                     "عفوا المستخدم مش موجود")
            applicant_vals.update({'employer': args.get("employer", False)})

            if not args.get('years_of_experience', False) <=0:
                return False, api_global_function.return_failed_request_vals(" Years Of Experience Not Valid",
                                                                             "عفوا سنوات  الخبرة غيرصالح")
            applicant_vals['years_of_experience'] = args.get('years_of_experience', False)

            if not args.get('workplace', False):
                return False, api_global_function.return_failed_request_vals(" Workplace Not provided",
                                                                             "عفوا  موقع العمل  مش موجود")
            applicant_vals.update({'workplace': args.get("workplace", False)})

            if not args.get('years_of_experience_in_haj', False) <=0:
                return False, api_global_function.return_failed_request_vals(" Years Of Experience  In Hag Works Not Valid",
                                                                             "عفوا سنوات  الخبرة في أعمال الحج غيرصالح")
            applicant_vals['years_of_experience_in_haj'] = args.get('years_of_experience_in_haj', False)

            if not args.get('job_title_in_haj', False):
                return False, api_global_function.return_failed_request_vals(
                    "Job Title In Haj  Not Provided",
                    "عفوا المسمى الوظيفي في الحج غير موجود ")
            if not self.env['hr.job'].sudo().search([('id', '=', args.get('job_title_in_haj', False))]):
                return False, api_global_function.return_failed_request_vals("Job Title In Haj  Not Correct",
                                                                                 "عفوا المسمى الوظيفي في الحج غير صحيح")
            applicant_vals['job_title_in_haj'] = args.get('job_title_in_haj', False)

            if not args.get('party_name_in_haj', False):
                return False, api_global_function.return_failed_request_vals(" Party Name In Haj Not provided",
                                                                             "عفوا الاسم المحدد في الحج  مش موجود")
            applicant_vals.update({'party_name_in_haj': args.get("party_name_in_haj", False)})

            if not args.get('job_app_announcement_id', False):
                return False, api_global_function.return_failed_request_vals(
                    "Job App Announcement Id Not Provided",
                    "عفوا المعلن عن تطبيق الوظيفة  غير موجود ")
            if not self.env['ipmc.application.announcement'].sudo().search([('id', '=', args.get('job_app_announcement_id', False))]):
                return False, api_global_function.return_failed_request_vals("Job App Announcement Id Not Provided",
                                                                             "عفوا المعلن عن تطبيق الوظيفة  غير موجود")
            applicant_vals['job_app_announcement_id'] = args.get('job_app_announcement_id', False)

            if not args.get('applied_job_workplace_id', False):
                return False, api_global_function.return_failed_request_vals(
                    "  Applied Job  WorkPlace Id Not Provided",
                    "عفوا المعلن عن  مكان العمل   غير موجود ")
            if not self.env['res.country.state'].sudo().search(
                    [('id', '=', args.get('applied_job_workplace_id', False))]):
                return False, api_global_function.return_failed_request_vals(" Applied Job  WorkPlace  Id Not Provided",
                                                                             "عفوا المعلن عن  مكان العمل   غير موجود")
            applicant_vals['applied_job_workplace_id'] = args.get('applied_job_workplace_id', False)

            if not args.get('first_job_id_applied', False):
                return False, api_global_function.return_failed_request_vals(
                    " First Job Id Applied Not Provided",
                    "عفوا المتقدم للوظيفة الأولى   غير موجود ")
            if not self.env['hr.job'].sudo().search([('id', '=', args.get('first_job_id_applied', False))]):
                return False, api_global_function.return_failed_request_vals("  First Job Id Applied Not Provided",
                                                                             "عفوا المتقدم للوظيفة الأولى  غير موجود")
            applicant_vals['first_job_id_applied'] = args.get('first_job_id_applied', False)

            if not args.get('first_job_sector_id', False):
                return False, api_global_function.return_failed_request_vals(
                    " First Job Sector Id  Not Provided",
                    "عفوامعرف قطاع الوظيفة الأولى  غير موجود ")
            if not self.env['hr.department'].sudo().search([('id', '=', args.get('first_job_sector_id', False))]):
                return False, api_global_function.return_failed_request_vals("  First Job Sector Id  Not Provided",
                                                                                     "عفوا معرف قطاع الوظيفة الأولى  غير موجود")
            applicant_vals['first_job_sector_id'] = args.get('first_job_sector_id', False)

            if not args.get('second_job_id_applied', False):
                return False, api_global_function.return_failed_request_vals(
                    " Second Job Id Applied  Not Provided",
                    "عفوامعرف قطاع الوظيفة الثانية  غير موجود ")
            if not self.env['hr.job'].sudo().search([('id', '=', args.get('second_job_id_applied', False))]):
                return False, api_global_function.return_failed_request_vals("  Second Job Id Applied  Not Provided",
                                                                             "عفوا معرف قطاع الوظيفة الثانية  غير موجود")
            applicant_vals['second_job_id_applied'] = args.get('second_job_id_applied', False)

            if not args.get('second_job_sector_id', False):
                return False, api_global_function.return_failed_request_vals(
                    " Second Job Sector Id  Not Provided",
                    "عفوامعرف قطاع الوظيفة الثانية  غير موجود ")
            if not self.env['hr.department'].sudo().search([('id', '=', args.get('second_job_sector_id', False))]):
                return False, api_global_function.return_failed_request_vals("  Second Job Sector Id  Not Provided",
                                                                             "عفوا معرف قطاع الوظيفة الثانية  غير موجود")
            applicant_vals['second_job_sector_id'] = args.get('second_job_sector_id', False)

            if not args.get('third_job_id_applied', False):
                return False, api_global_function.return_failed_request_vals(
                    " Third Job Id Applied  Not Provided",
                    "عفوامعرف قطاع الوظيفة الثالثة  غير موجود ")
            if not self.env['hr.job'].sudo().search([('id', '=', args.get('third_job_id_applied', False))]):
                return False, api_global_function.return_failed_request_vals("  Third Job Id Applied  Not Provided",
                                                                             "عفوا معرف قطاع الوظيفة الثالثة  غير موجود")
            applicant_vals['third_job_id_applied'] = args.get('third_job_id_applied', False)

            if not args.get('third_job_sector_id', False):
                return False, api_global_function.return_failed_request_vals(
                    " Third Job Sector Id  Not Provided",
                    "عفوامعرف قطاع الوظيفة الثالثة  غير موجود ")
            if not self.env['hr.department'].sudo().search([('id', '=', args.get('third_job_sector_id', False))]):
                return False, api_global_function.return_failed_request_vals("  Third Job Sector Id  Not Provided",
                                                                             "عفوا معرف قطاع الوظيفة الثالثة  غير موجود")
            applicant_vals['third_job_sector_id'] = args.get('third_job_sector_id', False)

            if not args.get('bank_id', False):
                return False, api_global_function.return_failed_request_vals(
                    " Bank Id  Not Provided",
                    "عفواموظف البنك  غير موجود ")
            if not self.env['res.bank'].sudo().search([('id', '=', args.get('bank_id', False))]):
                return False, api_global_function.return_failed_request_vals("  Bank Id  Not Provided",
                                                                             "عفوا موظف البنك  غير موجود")
            applicant_vals['bank_id'] = args.get('bank_id', False)

            if not args.get('iban', False):
                return False, api_global_function.return_failed_request_vals(" IBAN Number Not provided",
                                                                             "عفوا رقم IBAN مش موجود")
            applicant_vals.update({'iban': args.get("iban", False)})

            if not args.get('authorized_iban', False):
                return False, api_global_function.return_failed_request_vals(" IBAN Image Not provided",
                                                                             "عفوا صورة IBAN مش موجود")
            applicant_vals.update({'authorized_iban': args.get("authorized_iban", False)})

            if not args.get('profile_image', False):
                return False, api_global_function.return_failed_request_vals(" Profile Image Not provided",
                                                                             "عفوا صورة الملف الشخصي مش موجود")
            applicant_vals.update({'profile_image': args.get("profile_image", False)})

            if not args.get('cv', False):
                return False, api_global_function.return_failed_request_vals(" CV Not provided",
                                                                             "عفوا سيرتك الذاتية مش موجود")
            applicant_vals.update({'cv': args.get("cv", False)})

        except Exception as e:
            arabic_message = "%s  " % _(str(e)),
            englishmessage = "%s." % _(str(e))
            return False, api_global_function.return_failed_request_vals(englishmessage, arabic_message)
        return True, applicant_vals


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

