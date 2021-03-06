from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools
from openerp.tools.sql import drop_view_if_exists
import time
import math
from datetime import datetime
import datetime
from openerp import netsvc
import openerp.addons.decimal_precision as dp
from openerp import SUPERUSER_ID, netsvc
from _ast import Store
from datetime import timedelta
import datetime
import os
import xlsxwriter
from datetime import datetime
from dateutil import tz
from time import strftime
from datetime import date
from dateutil.relativedelta import relativedelta
from cairo._cairo import Context
from pytz import timezone


_logger = logging.getLogger(__name__) 
    
class employee_balance_scorecard(osv.osv):
    _name = "employee.balance.scorecard"
    _description = "Appraisal Form"
    _inherit = 'mail.thread'
    _track = {
        'state': {
            # 'hr_kra.mt_kra_submitted_to_employee': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'Waiting for Self Rate',
            # 'hr_kra.mt_kra_submitted_to_manager': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'Submitted To Manager',
            # 'hr_kra.mt_kra_submitted_to_mgmt': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'Submitted To Mgmt',
            'hr_kra.mt_kra_refused': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'Refused',
        },
              
        
    }
    
    #Financial Section Total Score 
    def _total_score_financial(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for score in self.browse(cr, uid, ids, context=context):
            total = 0.0
            for p in score.financial_kra_id:
                total = total+p.weighted_scoref
            res[score.id] = total
        return res
    
    #Customer Section Total Score
    def _total_score_customer(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for score in self.browse(cr, uid, ids, context=context):
            total = 0.0
            for p in score.customer_kra_id:
                total = total+p.weighted_scorec
            res[score.id] = total
        return res
    
    #Internal Process Section Total Score
    def _total_score_internal(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for score in self.browse(cr, uid, ids, context=context):
            total = 0.0
            for p in score.internal_kra_id:
                total = total+p.weighted_scorei
            res[score.id] = total
        return res
    
    #Learning Section Total Score
    def _total_score_learning(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for score in self.browse(cr, uid, ids, context=context):
            total = 0.0
            for p in score.learning_kra_id:
                total = total+p.weighted_scorel
            res[score.id] = total
        return res
    
    #Total Score of All sections
    def _total_score(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for w in self.browse(cr, uid, ids, context=context):
            total,totalf,totalc,totali,totall = 0.0,0.0,0.0,0.0,0.0
            for f in w.financial_kra_id:
                totalf = totalf+f.weighted_scoref
            for c in w.customer_kra_id:
                totalc = totalc+c.weighted_scorec
            for i in w.internal_kra_id:
                totali = totali+i.weighted_scorei
            for l in w.learning_kra_id:
                totall = totall+l.weighted_scorel
            total = totalc + totalf + totali + totall
            res[w.id] = total
        return res

    #Total of Self Rating of all Sections
    def _total_self_rating(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for w in self.browse(cr, uid, ids, context=context):
            total,totalf,totalc,totali,totall = 0.0,0.0,0.0,0.0,0.0
            for f in w.financial_kra_id:
                totalf = totalf+f.self_rating
            for c in w.customer_kra_id:
                totalc = totalc+c.self_rating
            for i in w.internal_kra_id:
                totali = totali+i.self_rating
            for l in w.learning_kra_id:
                totall = totall+l.self_rating
            total = totalc + totalf + totali + totall
            res[w.id] = total
        return res

    #Total of App Rating of All Sections
    def _total_app_rating(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for w in self.browse(cr, uid, ids, context=context):
            total,totalf,totalc,totali,totall = 0.0,0.0,0.0,0.0,0.0
            for f in w.financial_kra_id:
                totalf = totalf+f.app_rating
            for c in w.customer_kra_id:
                totalc = totalc+c.app_rating
            for i in w.internal_kra_id:
                totali = totali+i.app_rating
            for l in w.learning_kra_id:
                totall = totall+l.app_rating
            total = totalc + totalf + totali + totall
            res[w.id] = total
        return res

    #Total of Mgmt Rating of All Sections
    def _total_mgmt_rating(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for w in self.browse(cr, uid, ids, context=context):
            total,totalf,totalc,totali,totall = 0.0,0.0,0.0,0.0,0.0
            for f in w.financial_kra_id:
                totalf = totalf+f.mgmt_rating
            for c in w.customer_kra_id:
                totalc = totalc+c.mgmt_rating
            for i in w.internal_kra_id:
                totali = totali+i.mgmt_rating
            for l in w.learning_kra_id:
                totall = totall+l.mgmt_rating
            total = totalc + totalf + totali + totall
            res[w.id] = total
        return res
    
    #Total Weightage of Financial Section
    def _weightage_financial(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for w in self.browse(cr, uid, ids, context=context):
            total = 0.0
            for p in w.financial_kra_id:
                total = total+p.weightage
            res[w.id] = total
        print total, 'financial_weightage'
        return res

    #Total Weightage of Customer Section
    def _weightage_customer(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for w in self.browse(cr, uid, ids, context=context):
            total = 0.0
            for p in w.customer_kra_id:
                total = total+p.weightage
            res[w.id] = total
        print total, 'customer_weightage'
        return res
    
    #Total Weightage of Internal Section
    def _weightage_internal(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for w in self.browse(cr, uid, ids, context=context):
            total = 0.0
            for p in w.internal_kra_id:
                total = total+p.weightage
            res[w.id] = total
        print total, 'internal_weightage'
        return res
    
    #Total Weightage of Learning Section
    def _weightage_learning(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for w in self.browse(cr, uid, ids, context=context):
            total = 0.0
            for p in w.learning_kra_id:
                total = total+p.weightage
            res[w.id] = total
        print total, 'learning_weightage'
        return res
    
    #Total Weightage of all sections and check if its 100%
    def _weightage_total(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for w in self.browse(cr, uid, ids, context=context):
            total,totalf,totalc,totali,totall = 0.0,0.0,0.0,0.0,0.0
            for f in w.financial_kra_id:
                totalf = totalf+f.weightage
            for c in w.customer_kra_id:
                totalc = totalc+c.weightage
            for i in w.internal_kra_id:
                totali = totali+i.weightage
            for l in w.learning_kra_id:
                totall = totall+l.weightage
            total = totalc + totalf + totali + totall
            print total, 'totalllll'
            res[w.id] = total
        if total != 100 or total < 100:
            raise osv.except_osv(_('Warning!'),_('Total weightage should only be 100%'))
        return res
    
    def _file_read(self, cr, uid, location, fname, bin_size=False):
        r = ''
        try:
                if bin_size:
                        r = os.path.getsize(location)
                else:
                        r = open(location,'rb').read().encode('base64')
        except IOError:
                _logger.error("_read_file reading %s",location)
        return r

    def _retrieve_file(self, cr, uid, ids, name, value, arg, context=None):
        if context is None:
                context = {}
        result = {}
        attach = self.browse(cr, uid, ids[0], context=context)        
        bin_size = context.get('bin_size')
        if attach.file_url:
                result[attach.id] = self._file_read(cr, uid, attach.file_url, attach.file_name, bin_size)
        else:
                result[attach.id] = value
        return result

    #Constraint function to check if a duplicate record for any employee for a respective financial year exists or not.
    def check_existance(self, cr, uid, ids, context=None):
        if context is None:
                context = {}
        self_obj = self.browse(cr, uid, ids[0], context=context)
        field1 = self_obj.emp_name.id
        field2 = self_obj.appraisal_year.id
        search_ids = self.search(cr, uid, [('emp_name', '=', field1),('appraisal_year', '=' , field2)], context=context)
        res = True
        if len(search_ids) > 1:
            raise osv.except_osv(_('Warning!'),_('Appraisal form for %s for the financial year %s has been already processed')%(self_obj.emp_name.name,self_obj.appraisal_year.name))
            res = False
        return res

    def _app_yr_get(self, cr, uid, context=None):
        today = datetime.today().date()
        yrs = self.pool.get('account.fiscalyear')
        if str(today)>='2016-02-01' and str(today)<='2016-06-30':
            search_add_id = yrs.search(cr,uid,[('name','=','2015-2016')])
        elif str(today)>='2017-02-01' and str(today)<='2017-06-30':
            search_add_id = yrs.search(cr,uid,[('name','=','2016-2017')])  
        else:
            search_add_id = ''
        return search_add_id[0]

    _columns = {
        'company_id': fields.many2one('res.company', 'Company'),
        'name': fields.char('Description'),
        'appraisal_year': fields.many2one('account.fiscalyear', 'Appraisal Year', required=True, select=True),
        'date_kra': fields.date('Date', select=True),
        'date_after_7Days': fields.date('Date'),
        'financial_kra_id': fields.one2many('balance.scorecard.financial','financial_id', 'Financial'),
        'customer_kra_id': fields.one2many('balance.scorecard.customer','cust_id', 'Customer'),
        'internal_kra_id': fields.one2many('balance.scorecard.internal','internal_id', 'Internal Process'),
        'learning_kra_id': fields.one2many('balance.scorecard.learning','learning_id', 'Learning & Growth'),
        'company_id': fields.many2one('res.company', 'Company'),
        
        'emp_name': fields.many2one('hr.employee', "Employee Name", required=True),
        'emp_code': fields.char('Employee Code'),
        'department': fields.many2one('hr.department', "Department", required=True),
        'join_date': fields.date("Date Of Joining"),
        'job': fields.many2one('hr.job', 'Designation'),
        'manager_id': fields.many2one('hr.employee', 'Reporting To', required=True, domain="[('manager', '=', True)]"),
        'total_score_financial':fields.function(_total_score_financial,string ='Total Score',store=True),
        'total_score_customer':fields.function(_total_score_customer,string ='Total Score',store=True),
        'total_score_internal':fields.function(_total_score_internal,string ='Total Score',store=True),
        'total_score_learning':fields.function(_total_score_learning,string ='Total Score',store=True),
        'total_score':fields.function(_total_score,string ='Total Weighted Score',store=True),
        'total_self_rating':fields.function(_total_self_rating,string ='Self Rating',store=True),
        'total_app_rating':fields.function(_total_app_rating,string ='Appraiser Rating',store=True),
        'total_mgmt_rating':fields.function(_total_mgmt_rating,string ='Mgmt Rating',store=True),
        'weightage_financial':fields.function(_weightage_financial,string='Weightage (in %)',store=True),
        'weightage_customer':fields.function(_weightage_customer,string='Weightage (in %)',store=True),
        'weightage_internal':fields.function(_weightage_internal,string='Weightage (in %)',store=True),
        'weightage_learning':fields.function(_weightage_learning,string='Weightage (in %)',store=True),
        'total_weightage':fields.function(_weightage_total,string='Total Weightage (in %)',store=True),
        'location': fields.char('Location'),
        'state': fields.selection([('New', 'New'),('Waiting for Self Rate','Waiting for Self Rating'),('Self Rating Given','Self Rating Given'),('Submitted To Manager', 'Submitted To Manager'),('Appraisal Meeting','Appraisal Meeting'),('Waiting Manager Approval', "Manager's Rating"),('Submitted To Mgmt', 'Submitted To Mgmt'),('Reviewed By Mgmt', 'Reviewed By Mgmt'),('Publish','Published'),('Refused','Refused')], 'Status'),    
        'to_be_promoted': fields.boolean('To be Promoted'),
        'export_file': fields.function(_retrieve_file, type='binary', string='File', nodrop=True, readonly=True),
        'file_url':fields.char('File URL'),
        'file_name':fields.char('File Name'),
        'current_user':fields.many2one('res.users','Current User',size=32),   
        'specify_reason_for_refusal':fields.boolean('Specify Reason for Refusal of KRA'),
        'reason_for_refusal':fields.text('Reason for Refusal of KRA'), 
        'meeting_ok': fields.boolean('Meeting Ok') 
    }
    
    _defaults = {
            'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'employee.balance.scorecard', context=c),
            'state': 'New',
            'appraisal_year': _app_yr_get,
            'date_kra': fields.date.context_today,
            'current_user': lambda obj, cr, uid, ctx=None: uid,
            'meeting_ok': False,
            'name': 'Appraisal Process ',

        }
    
    _constraints = [(check_existance,'Appraisal form for the employee for the given financial year has been already processed', ['emp_name','appraisal_year'])]

    def onchange_employee(self, cr, uid, ids, emp_name, context=None):
        value = {'join_date': False,'department': False, 'job': False, 'emp_code': False, 'manager_id': False,'appraisal_year':False}
        if emp_name:
            emp = self.pool.get('hr.employee').browse(cr, uid, emp_name)
            value['join_date'] = emp.join_date
            value['department'] = emp.department_id.id
            value['job'] = emp.job_id.id
            value['emp_code'] = emp.auto_emp_code
            value['manager_id'] = emp.parent_id.id
            today = datetime.today().date()
            yrs = self.pool.get('account.fiscalyear')
            if str(today)>='2015-04-01' and str(today)<='2016-03-31':
                search_add_id = yrs.search(cr,uid,[('name','=','2015-2016')])
                value['appraisal_year'] = search_add_id
            elif str(today)>='2016-04-01' and str(today)<='2017-03-31':
                search_add_id = yrs.search(cr,uid,[('name','=','2016-2017')])
                value['appraisal_year'] = search_add_id
            else:
                value['appraisal_year'] = ''
        return {'value': value}
    
    
    def create(self, cr, uid, vals, context=None):
        import time
        from datetime import date
        from datetime import datetime
        if vals.has_key('name') and vals.has_key('emp_name'):
            print vals['emp_name']            
            x = self.pool.get('hr.employee').search(cr,uid,[('id','=', vals['emp_name'])])
            for m in self.pool.get('hr.employee').browse(cr,uid,x):
                name = m.name
            if vals['name'] or vals['emp_name']:
                vals['name'] = vals['name'] + " for " + str(name)
                vals.update({'name':vals['name']})
        res_id = super(employee_balance_scorecard, self).create(cr, uid, vals, context)
        return res_id


    def write(self, cr, uid, ids, vals, context=None):
        res_id = super(employee_balance_scorecard, self).write(cr, uid, ids, vals, context=context)
        nm1 = ''
        if isinstance(ids, list):
            main_form_id = ids
        else:
            main_form_id = [ids]
        for h in self.browse(cr,uid,main_form_id,context):
            nm = h.name
            emp = h.emp_name.name
            print nm, 'namemmm'
            nm = nm.split('for')
        nm1 = nm[0] + "for " + emp
        res_id = super(employee_balance_scorecard, self).write(cr, uid, main_form_id, {'name':nm1}, context=context)
        return res_id


    def unlink(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context=context):
            # search_hro = self.pool.get('res.users').search(cr, uid, [('is_hro', '=', True)])
            # print rec.emp_name.hro.id
            # print uid, 'hroooo IDDD'
            if rec.emp_name.hro.id != uid:
                raise osv.except_osv(_('Warning!'),_('You cannot delete Appraisal record'))
            if rec.state != 'New':
                raise osv.except_osv(_('Warning!'),_('You can only delete draft Appraisal record!'))
        return super(employee_balance_scorecard, self).unlink(cr, uid, ids, context)

    #Scheduler function to remind employee to give self ratings in the KRA record
    def reminder_give_self_rating(self, cr, uid, context=None):
        print 'in the self rating reminder'
        rec_search = self.search(cr, uid, [('id', '>', 0),('state','=','Waiting for Self Rate')], context=None)
        print rec_search
        for x in self.browse(cr,uid,rec_search):
            count = 0
            id_form = x.id
            current_state = x.state
            current_id = x.id
            kra_date = x.date_kra   
            print x.date_kra
            print x.state
            print id_form, 'form_id'
            if kra_date:
                new_kra_date = datetime.strptime(str(kra_date), "%Y-%m-%d").date()
                
                today = datetime.today().date()
                print today, 'today'
                tenure = relativedelta(today,new_kra_date)
                print tenure.days, 'tenuree days'
                print tenure
                if current_state == "Waiting for Self Rate" and tenure.days in (2,4,6):
                    search_template_record = self.pool.get('email.template').search(cr,uid,[('model_id.model','=','employee.balance.scorecard'),('lang','=','Give Self Rating 2Days')], context=context)
                    if search_template_record:
                            print "ggggggggggggggggggggggggggggggggggggggggggggggg", search_template_record
                            print 'I am intoooo self rating reminder definition'
                            self.pool.get('email.template').send_mail(cr, uid, search_template_record[0], current_id, force_send=True, context=context)
                            print "Send Reminder"
                            count = count+1
                            return True
                if current_state == "Waiting for Self Rate" and tenure.days == 7:
                    search_template_record = self.pool.get('email.template').search(cr,uid,[('model_id.model','=','employee.balance.scorecard'),('lang','=','Give Self Rating 7Days')], context=context)
                    if search_template_record:
                            print "ggggggggggggggggggggggggggggggggggggggggggggggg", search_template_record
                            print 'I am intoooo self rating reminder definition'
                            self.pool.get('email.template').send_mail(cr, uid, search_template_record[0], current_id, force_send=True, context=context)
                            print "Send Reminder"
                            count = count+1
                            return True


    def reminder_to_schedule_appraisal_meeting(self, cr, uid, context=None):
        print 'in the self rating reminder'
        rec_search = self.search(cr, uid, [('id', '>', 0),('state','=','Submitted To Manager')], context=None)
        print rec_search
        kra_interview_obj = self.pool.get('kra.interview')
        for x in self.browse(cr,uid,rec_search):
            count = 0
            id_form = x.id
            current_state = x.state
            current_id = x.id
            kra_date = x.date_kra
            emp_name = x.emp_name.id
            appraisal_year = x.appraisal_year.id   
            print x.date_kra
            print x.state
            print id_form, 'form_id'
            if kra_date:
                new_kra_date = datetime.strptime(str(kra_date), "%Y-%m-%d").date()
                today = datetime.today().date()
                print today, 'today'
                tenure = relativedelta(today,new_kra_date)
                print tenure.days, 'tenuree days'
                print tenure
                search_ids = kra_interview_obj.search(cr, uid, [('user_to_review_id', '=', emp_name),('appraisal_year', '=' , appraisal_year)], context=context)
                print search_ids, 'fresh check of reminder'
                if current_state == "Submitted To Manager" and tenure.days in (2,4,6,7) and search_ids == []:
                    search_template_record = self.pool.get('email.template').search(cr,uid,[('model_id.model','=','employee.balance.scorecard'),('lang','=','Schedule Appraisal Meeting')], context=context)
                    if search_template_record:
                            self.pool.get('email.template').send_mail(cr, uid, search_template_record[0], current_id, force_send=True, context=context)
                            print "Send Reminder"
                            count = count+1
                            return True


    #Scheduler function to remind Reporting Manager to give self ratings in the KRA record
    def reminder_give_appraiser_rating(self, cr, uid, context=None):
        print 'in the appraiser rating reminder'
        rec_search = self.search(cr, uid, [('id', '>', 0),('state','in',('Appraisal Meeting','Waiting Manager Approval'))], context=None)
        print rec_search, 'Rec Searchhhh'
        kra_interview_obj = self.pool.get('kra.interview')
        for x in self.browse(cr,uid,rec_search):
            count = 0
            id_form = x.id
            emp_name = x.emp_name.id
            appraisal_year = x.appraisal_year.id
            current_state = x.state
            current_id = x.id
            kra_date = x.date_kra   
            print x.date_kra
            print x.state
            print id_form, 'form_id'
            search_ids = kra_interview_obj.search(cr, uid, [('user_to_review_id', '=', emp_name),('appraisal_year', '=' , appraisal_year)], context=context)
            print search_ids, 'search_ids'
            if search_ids:
                for m in kra_interview_obj.browse(cr,uid,search_ids):
                    review_state = m.state
                    interview_date = m.date_interview
                    new_interview_date = datetime.strptime(str(interview_date[0:10]), "%Y-%m-%d").date()
                    today = datetime.now()
                    today = datetime.today().date()
                    tenure = relativedelta(today,new_interview_date)
                    if review_state == 'done' and tenure.days in (2,4,6):
                        search_template_record = self.pool.get('email.template').search(cr,uid,[('model_id.model','=','employee.balance.scorecard'),('lang','=','Appraiser Reminder')], context=context)
                        if search_template_record:
                            self.pool.get('email.template').send_mail(cr, uid, search_template_record[0], current_id, force_send=True, context=context)
                            print "Send Reminder"
                            count = count+1
                            return True
                    if review_state == 'done' and tenure.days == 7:
                        search_template_record = self.pool.get('email.template').search(cr,uid,[('model_id.model','=','employee.balance.scorecard'),('lang','=','Appraiser Reminder7')], context=context)
                        if search_template_record:
                            self.pool.get('email.template').send_mail(cr, uid, search_template_record[0], current_id, force_send=True, context=context)
                            print "Send Reminder"
                            count = count+1
                            return True


                
    
    #Function for submitting the KRA record By HR to Employee
    def submit_for_self_rate(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        form_id = x.id
        emp_name = x.emp_name.id
        designation = x.job.id
        department = x.department.id
        emp_code = x.emp_code
        manager = x.manager_id.id
        join_date = x.join_date
        search_f = x.financial_kra_id
        search_c = x.customer_kra_id
        search_i = x.internal_kra_id
        search_l = x.learning_kra_id
        if not search_f:
            raise osv.except_osv(_('Warning!'),_('Financial Section cannot be empty'))
        if not search_c:
            raise osv.except_osv(_('Warning!'),_('Customer Section cannot be empty'))
        if not search_i:
            raise osv.except_osv(_('Warning!'),_('Internal Process Section cannot be empty'))
        if not search_l:
            raise osv.except_osv(_('Warning!'),_('Learning & Growth Section cannot be empty'))
        total = 0.0
        total = x.weightage_financial + x.weightage_customer + x.weightage_internal + x.weightage_learning
        if total != 100 or total < 100 or total > 100:
            raise osv.except_osv(_('Warning!'),_('Total weightage should only be 100%'))
        subscribe_ids = []
        if x.emp_name and x.emp_name.parent_id and x.emp_name.parent_id.user_id:
            subscribe_ids = [x.emp_name.parent_id.user_id.id,x.emp_name.hro.id,52]  
        self.message_subscribe_users(cr, SUPERUSER_ID, [x.id], user_ids=subscribe_ids, context=context)
        message = _("Appraisal form submitted to %s for Self Rating.") % (x.emp_name.name)
        self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        # message = _("Hi %s, <br>You are requested to give the self rating in your own Performance Review form. Kindly rate yourself for each KRA point on a scale of 1 to 5") % (x.emp_name.name)
        # self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        search_valuef = self.pool.get('balance.scorecard.financial').search(cr,uid,[('financial_id','=',form_id)])
        search_valuec = self.pool.get('balance.scorecard.customer').search(cr,uid,[('cust_id','=',form_id)])
        search_valuei = self.pool.get('balance.scorecard.internal').search(cr,uid,[('internal_id','=',form_id)])
        search_valuel = self.pool.get('balance.scorecard.learning').search(cr,uid,[('learning_id','=',form_id)])
        for m in self.pool.get('balance.scorecard.financial').browse(cr,uid,search_valuef):
            if m.weightage == 0.0:
                raise osv.except_osv(_('Warning!'),_('In Financial Section, weightage cannot be 0%'))
            self.pool.get('balance.scorecard.financial').write(cr,uid,m.id,{'statef':'Waiting for Self Rate'})
        for m in self.pool.get('balance.scorecard.customer').browse(cr,uid,search_valuec):
            if m.weightage == 0.0:
                raise osv.except_osv(_('Warning!'),_('In Customer Section, weightage cannot be 0%'))
            self.pool.get('balance.scorecard.customer').write(cr,uid,m.id,{'statef':'Waiting for Self Rate'})
        for m in self.pool.get('balance.scorecard.internal').browse(cr,uid,search_valuei):
            if m.weightage == 0.0:
                raise osv.except_osv(_('Warning!'),_('In Internal Process Section, weightage cannot be 0%'))
            self.pool.get('balance.scorecard.internal').write(cr,uid,m.id,{'statef':'Waiting for Self Rate'})
        for m in self.pool.get('balance.scorecard.learning').browse(cr,uid,search_valuel):
            if m.weightage == 0.0:
                raise osv.except_osv(_('Warning!'),_('In Learning & Growth Section, weightage cannot be 0%'))
            self.pool.get('balance.scorecard.learning').write(cr,uid,m.id,{'statef':'Waiting for Self Rate'})
        today = datetime.today().date()
        date_after_7Days = today + timedelta(days=7)
	self.write(cr, uid, ids, {'state': 'Waiting for Self Rate','date_kra':today,'date_after_7Days':date_after_7Days}, context=context)
        search_self_submit_email_template = self.pool.get('email.template').search(cr,uid,[('model_id.model','=','employee.balance.scorecard'),('lang','=','Self Rating')], context=context)
        if search_self_submit_email_template:
            send_self_rating_submit_mail = self.pool.get('email.template').send_mail(cr, uid, search_self_submit_email_template[0], ids[0], force_send=True, context=context)
        
        
        




    #Function when Employee Submits the KRA record from waiting for self rate to self rating given state
    def submit(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        form_id = x.id
        search_valuef = self.pool.get('balance.scorecard.financial').search(cr,uid,[('financial_id','=',form_id)])
        search_valuec = self.pool.get('balance.scorecard.customer').search(cr,uid,[('cust_id','=',form_id)])
        search_valuei = self.pool.get('balance.scorecard.internal').search(cr,uid,[('internal_id','=',form_id)])
        search_valuel = self.pool.get('balance.scorecard.learning').search(cr,uid,[('learning_id','=',form_id)])
        hro_user_id = x.emp_name.hro.id
        if x.emp_name.user_id.id != uid:
            raise osv.except_osv(_('Warning!'),_('You cannot give self rating for your subordinate'))
                
        for m in self.pool.get('balance.scorecard.financial').browse(cr,uid,search_valuef):
            if m.self_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
                raise osv.except_osv(_('Warning!'),_('In Financial Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the self rating column'))
            self.pool.get('balance.scorecard.financial').write(cr,uid,m.id,{'statef':'Self Rating Given'})
        for m in self.pool.get('balance.scorecard.customer').browse(cr,uid,search_valuec):
            if m.self_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
                raise osv.except_osv(_('Warning!'),_('In Customer Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the self rating column'))
            self.pool.get('balance.scorecard.customer').write(cr,uid,m.id,{'statef':'Self Rating Given'})
        for m in self.pool.get('balance.scorecard.internal').browse(cr,uid,search_valuei):
            if m.self_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
                raise osv.except_osv(_('Warning!'),_('In Internal Process Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the self rating column'))
            self.pool.get('balance.scorecard.internal').write(cr,uid,m.id,{'statef':'Self Rating Given'})
        for m in self.pool.get('balance.scorecard.learning').browse(cr,uid,search_valuel):
            if m.self_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
                raise osv.except_osv(_('Warning!'),_('In Learning & Growth Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the self rating column'))
            self.pool.get('balance.scorecard.learning').write(cr,uid,m.id,{'statef':'Self Rating Given'})
        return self.write(cr, uid, ids, {'state': 'Self Rating Given'}, context=context)
    
    #Function when employee submits the KRA record to his Reporting Manager
    def submit_kra(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        form_id = x.id
        subscribe_ids = []
        if x.emp_name and x.emp_name.parent_id and x.emp_name.parent_id.user_id:
            subscribe_ids = [x.emp_name.parent_id.user_id.id,x.emp_name.hro.id,52]  
        self.message_subscribe_users(cr, SUPERUSER_ID, [x.id], user_ids=subscribe_ids, context=context)        
        message = _("Hi, <br>%s has submitted Appraisal form with self rating. <br>Kindly schedule Appraisal Meeting for Appraiser Rating.") % (x.emp_name.name)
        self.message_post(cr, x.emp_name.hro.id, ids, body = message, type='comment', subtype='mt_comment', context = context)
        search_valuef = self.pool.get('balance.scorecard.financial').search(cr,uid,[('financial_id','=',form_id)])
        search_valuec = self.pool.get('balance.scorecard.customer').search(cr,uid,[('cust_id','=',form_id)])
        search_valuei = self.pool.get('balance.scorecard.internal').search(cr,uid,[('internal_id','=',form_id)])
        search_valuel = self.pool.get('balance.scorecard.learning').search(cr,uid,[('learning_id','=',form_id)])
        for m in self.pool.get('balance.scorecard.financial').browse(cr,uid,search_valuef):
            self.pool.get('balance.scorecard.financial').write(cr,uid,m.id,{'statef':'Submitted To Manager'})
        for m in self.pool.get('balance.scorecard.customer').browse(cr,uid,search_valuec):
            self.pool.get('balance.scorecard.customer').write(cr,uid,m.id,{'statef':'Submitted To Manager'})
        for m in self.pool.get('balance.scorecard.internal').browse(cr,uid,search_valuei):
            self.pool.get('balance.scorecard.internal').write(cr,uid,m.id,{'statef':'Submitted To Manager'})
        for m in self.pool.get('balance.scorecard.learning').browse(cr,uid,search_valuel):
            self.pool.get('balance.scorecard.learning').write(cr,uid,m.id,{'statef':'Submitted To Manager'})
        today = datetime.today().date()
        date_after_7Days = today + timedelta(days=7)
        search_self_submit_email_template = self.pool.get('email.template').search(cr,uid,[('model_id.model','=','employee.balance.scorecard'),('lang','=','KRA Self Rating')], context=context)
        if search_self_submit_email_template:
            send_self_rating_submit_mail = self.pool.get('email.template').send_mail(cr, uid, search_self_submit_email_template[0], ids[0], force_send=True, context=context)
        search_self_submit_email_template_1 = self.pool.get('email.template').search(cr,uid,[('model_id.model','=','employee.balance.scorecard'),('lang','=','KRA Self Rating to HR')], context=context)
        if search_self_submit_email_template_1:
            send_self_rating_submit_mail = self.pool.get('email.template').send_mail(cr, uid, search_self_submit_email_template_1[0], ids[0], force_send=True, context=context)
        return self.write(cr, uid, ids, {'state': 'Submitted To Manager','date_kra':today,'date_after_7Days':date_after_7Days}, context=context)

    #Function when Reporting Manager submits the KRA record to the Management
    def submit_mgmt(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        form_id = x.id
        if x.emp_name and x.emp_name.parent_id and x.emp_name.parent_id.user_id:
            subscribe_ids = [x.emp_name.parent_id.user_id.id,x.emp_name.hro.id,52]  
        self.message_subscribe_users(cr, SUPERUSER_ID, [x.id], user_ids=subscribe_ids, context=context)
        if x.emp_name.user_id.id == uid:
            raise osv.except_osv(_('Warning!'),_('You cannot give Appraiser rating for your own Performance'))
        search_valuef = self.pool.get('balance.scorecard.financial').search(cr,uid,[('financial_id','=',form_id)])
        search_valuec = self.pool.get('balance.scorecard.customer').search(cr,uid,[('cust_id','=',form_id)])
        search_valuei = self.pool.get('balance.scorecard.internal').search(cr,uid,[('internal_id','=',form_id)])
        search_valuel = self.pool.get('balance.scorecard.learning').search(cr,uid,[('learning_id','=',form_id)])
        for m in self.pool.get('balance.scorecard.financial').browse(cr,uid,search_valuef):
            if m.app_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
                raise osv.except_osv(_('Warning!'),_('In Financial Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the Appraiser rating column'))
            self.pool.get('balance.scorecard.financial').write(cr,uid,m.id,{'statef':'Submitted To Mgmt'})
        for m in self.pool.get('balance.scorecard.customer').browse(cr,uid,search_valuec):
            if m.app_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
                raise osv.except_osv(_('Warning!'),_('In Customer Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the Appraiser rating column'))
            self.pool.get('balance.scorecard.customer').write(cr,uid,m.id,{'statef':'Submitted To Mgmt'})
        for m in self.pool.get('balance.scorecard.internal').browse(cr,uid,search_valuei):
            if m.app_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
                raise osv.except_osv(_('Warning!'),_('In Internal Process Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the Appraiser rating column'))
            self.pool.get('balance.scorecard.internal').write(cr,uid,m.id,{'statef':'Submitted To Mgmt'})
        for m in self.pool.get('balance.scorecard.learning').browse(cr,uid,search_valuel):
            if m.app_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
                raise osv.except_osv(_('Warning!'),_('In Learning & Growth Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the Appraiser rating column'))
            self.pool.get('balance.scorecard.learning').write(cr,uid,m.id,{'statef':'Submitted To Mgmt'})
        message = _("Hi, <p>%s has completed the Appraiser Rating for %s and has submitted it to the Management.") % (x.emp_name.parent_id.name, x.emp_name.name)
        self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        return self.write(cr, uid, ids, {'state': 'Submitted To Mgmt'}, context=context)

    #Function when Management Approves the KRA record
    def approve_kra_mgmt(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        subscribe_ids = []
        if x.emp_name and x.emp_name.parent_id and x.emp_name.parent_id.user_id:
            subscribe_ids = [x.emp_name.parent_id.user_id.id,x.emp_name.hro.id,52]  
        self.message_subscribe_users(cr, SUPERUSER_ID, [x.id], user_ids=subscribe_ids, context=context)
        message = _("Appraisal form for %s, is reviewed by Management, you may proceed to Publish the Appraisal data.") % (x.emp_name.name)
        self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        form_id = x.id
        search_valuef = self.pool.get('balance.scorecard.financial').search(cr,uid,[('financial_id','=',form_id)])
        search_valuec = self.pool.get('balance.scorecard.customer').search(cr,uid,[('cust_id','=',form_id)])
        search_valuei = self.pool.get('balance.scorecard.internal').search(cr,uid,[('internal_id','=',form_id)])
        search_valuel = self.pool.get('balance.scorecard.learning').search(cr,uid,[('learning_id','=',form_id)])
        for m in self.pool.get('balance.scorecard.financial').browse(cr,uid,search_valuef):
            if m.mgmt_rating == 0.0:
                pass
            elif m.mgmt_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
                raise osv.except_osv(_('Warning!'),_('In Financial Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the Mgmt rating column'))
            self.pool.get('balance.scorecard.financial').write(cr,uid,m.id,{'statef':'Reviewed By Mgmt'})
        for m in self.pool.get('balance.scorecard.customer').browse(cr,uid,search_valuec):
            if m.mgmt_rating == 0.0:
                pass
            elif m.mgmt_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
                raise osv.except_osv(_('Warning!'),_('In Customer Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the Mgmt rating column'))
            self.pool.get('balance.scorecard.customer').write(cr,uid,m.id,{'statef':'Reviewed By Mgmt'})
        for m in self.pool.get('balance.scorecard.internal').browse(cr,uid,search_valuei):
            if m.mgmt_rating == 0.0:
                pass
            elif m.mgmt_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
                raise osv.except_osv(_('Warning!'),_('In Internal Process Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the Mgmt rating column'))
            self.pool.get('balance.scorecard.internal').write(cr,uid,m.id,{'statef':'Reviewed By Mgmt'})
        for m in self.pool.get('balance.scorecard.learning').browse(cr,uid,search_valuel):
            if m.mgmt_rating == 0.0:
                pass
            elif m.mgmt_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
                raise osv.except_osv(_('Warning!'),_('In Learning & Growth Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the Mgmt rating column'))
            self.pool.get('balance.scorecard.learning').write(cr,uid,m.id,{'statef':'Reviewed By Mgmt'})
        return self.write(cr, uid, ids, {'state': 'Reviewed By Mgmt'}, context=context)

    def appraisal_meeting(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        form_id = x.id
        search_valuef = self.pool.get('balance.scorecard.financial').search(cr,uid,[('financial_id','=',form_id)])
        search_valuec = self.pool.get('balance.scorecard.customer').search(cr,uid,[('cust_id','=',form_id)])
        search_valuei = self.pool.get('balance.scorecard.internal').search(cr,uid,[('internal_id','=',form_id)])
        search_valuel = self.pool.get('balance.scorecard.learning').search(cr,uid,[('learning_id','=',form_id)])
        for m in self.pool.get('balance.scorecard.financial').browse(cr,uid,search_valuef):
            self.pool.get('balance.scorecard.financial').write(cr,uid,m.id,{'statef':'Appraisal Meeting'})
        for m in self.pool.get('balance.scorecard.customer').browse(cr,uid,search_valuec):
            self.pool.get('balance.scorecard.customer').write(cr,uid,m.id,{'statef':'Appraisal Meeting'})
        for m in self.pool.get('balance.scorecard.internal').browse(cr,uid,search_valuei):
            self.pool.get('balance.scorecard.internal').write(cr,uid,m.id,{'statef':'Appraisal Meeting'})
        for m in self.pool.get('balance.scorecard.learning').browse(cr,uid,search_valuel):
            self.pool.get('balance.scorecard.learning').write(cr,uid,m.id,{'statef':'Appraisal Meeting'})
        return self.write(cr, uid, ids, {'state': 'Appraisal Meeting'}, context=context)


    def give_app_rating(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        form_id = x.id
        search_valuef = self.pool.get('balance.scorecard.financial').search(cr,uid,[('financial_id','=',form_id)])
        search_valuec = self.pool.get('balance.scorecard.customer').search(cr,uid,[('cust_id','=',form_id)])
        search_valuei = self.pool.get('balance.scorecard.internal').search(cr,uid,[('internal_id','=',form_id)])
        search_valuel = self.pool.get('balance.scorecard.learning').search(cr,uid,[('learning_id','=',form_id)])
        for m in self.pool.get('balance.scorecard.financial').browse(cr,uid,search_valuef):
            self.pool.get('balance.scorecard.financial').write(cr,uid,m.id,{'statef':'Waiting Manager Approval'})
        for m in self.pool.get('balance.scorecard.customer').browse(cr,uid,search_valuec):
            self.pool.get('balance.scorecard.customer').write(cr,uid,m.id,{'statef':'Waiting Manager Approval'})
        for m in self.pool.get('balance.scorecard.internal').browse(cr,uid,search_valuei):
            self.pool.get('balance.scorecard.internal').write(cr,uid,m.id,{'statef':'Waiting Manager Approval'})
        for m in self.pool.get('balance.scorecard.learning').browse(cr,uid,search_valuel):
            self.pool.get('balance.scorecard.learning').write(cr,uid,m.id,{'statef':'Waiting Manager Approval'})
        return self.write(cr, uid, ids, {'state':'Waiting Manager Approval'}, context=context)

    def publish_kra(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        form_id = x.id
        search_valuef = self.pool.get('balance.scorecard.financial').search(cr,uid,[('financial_id','=',form_id)])
        search_valuec = self.pool.get('balance.scorecard.customer').search(cr,uid,[('cust_id','=',form_id)])
        search_valuei = self.pool.get('balance.scorecard.internal').search(cr,uid,[('internal_id','=',form_id)])
        search_valuel = self.pool.get('balance.scorecard.learning').search(cr,uid,[('learning_id','=',form_id)])
        for m in self.pool.get('balance.scorecard.financial').browse(cr,uid,search_valuef):
            self.pool.get('balance.scorecard.financial').write(cr,uid,m.id,{'statef':'Publish'})
        for m in self.pool.get('balance.scorecard.customer').browse(cr,uid,search_valuec):
            self.pool.get('balance.scorecard.customer').write(cr,uid,m.id,{'statef':'Publish'})
        for m in self.pool.get('balance.scorecard.internal').browse(cr,uid,search_valuei):
            self.pool.get('balance.scorecard.internal').write(cr,uid,m.id,{'statef':'Publish'})
        for m in self.pool.get('balance.scorecard.learning').browse(cr,uid,search_valuel):
            self.pool.get('balance.scorecard.learning').write(cr,uid,m.id,{'statef':'Publish'})
        message = _("Appraisal data for %s has been published in the ERP.") % (x.emp_name.name)
        self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        search_self_submit_email_template = self.pool.get('email.template').search(cr,uid,[('model_id.model','=','employee.balance.scorecard'),('lang','=','KRA Data')], context=context)
        if search_self_submit_email_template:
            send_self_rating_submit_mail = self.pool.get('email.template').send_mail(cr, uid, search_self_submit_email_template[0], ids[0], force_send=True, context=context)
        self.write(cr, uid, ids, {'state': 'Publish'}, context=context)
        # assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        # ir_model_data = self.pool.get('ir.model.data')
        # try:
        #     template_id = ir_model_data.get_object_reference(cr, uid, 'hr_kra', 'email_template_edi_kra_publish')[1]
        # except ValueError:
        #     template_id = False
        # try:
        #     compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        # except ValueError:
        #     compose_form_id = False 
        # ctx = dict(context)
        # ctx.update({
        #     'default_model': 'employee.balance.scorecard',
        #     'default_res_id': ids[0],
        #     'default_template_id': template_id,
        #     'default_composition_mode': 'comment',
        #     # 'default_state': 'Publish',
        # })
        # return {
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'mail.compose.message',
        #     'views': [(compose_form_id, 'form')],
        #     'view_id': compose_form_id,
        #     'target': 'new',
        #     'context': ctx,
        # }


    def take_appraisal_meeting(self, cr, uid, ids, context=None):
        self_obj = self.browse(cr, uid, ids[0], context=context)
        for x in self.browse(cr, uid, ids, context=None):
            form_id = x.id
            emp_name = int(x.emp_name)
            appYr = int(x.appraisal_year)
        field1 = self_obj.emp_name.id
        field2 = self_obj.appraisal_year.id
        # self.write(cr, uid, ids, {'meeting_ok': True}, context=context)
        if x.emp_name.user_id.id == uid:
            raise osv.except_osv(_('Warning!'),_('You cannot schedule your own Appraisal Meeting'))
        search_ids = self.pool.get('kra.interview').search(cr, uid, [('user_to_review_id', '=', field1),('appraisal_year', '=' , field2)], context=context)
        print search_ids , 'seaaarchhh'
        res = True
        if len(search_ids) >= 1:
            raise osv.except_osv(_('Warning!'),_('Appraisal Meeting record for %s for the financial year %s has been already processed')%(self_obj.emp_name.name,self_obj.appraisal_year.name))
        context.update({'default_user_to_review_id': emp_name})
        if not ids: return False
        if not isinstance(ids, list): ids = [ids]
        ir_model_data = self.pool.get('ir.model.data')        
        view_ref = ir_model_data.get_object_reference(cr, uid, 'hr_kra', 'view_kra_interview_form')
        view_id = view_ref and view_ref[1] or False,
        return {
           'type': 'ir.actions.act_window',
           'name': 'Review Requests',
           'context': context,
           'view_mode': 'form',
           'view_type': 'form',
           'view_id': view_id,
           'res_model': 'kra.interview',
           'nodestroy': False,
           'target': 'current',
        }       

    #Function when KRA record is refused
    def refuse_request(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        form_id = x.id
        specify_reason_for_refusal = x.specify_reason_for_refusal
        reason_for_refusal = x.reason_for_refusal
        
        search_valuef = self.pool.get('balance.scorecard.financial').search(cr,uid,[('financial_id','=',form_id)])
        search_valuec = self.pool.get('balance.scorecard.customer').search(cr,uid,[('cust_id','=',form_id)])
        search_valuei = self.pool.get('balance.scorecard.internal').search(cr,uid,[('internal_id','=',form_id)])
        search_valuel = self.pool.get('balance.scorecard.learning').search(cr,uid,[('learning_id','=',form_id)])
        for m in self.pool.get('balance.scorecard.financial').browse(cr,uid,search_valuef):
            self.pool.get('balance.scorecard.financial').write(cr,uid,m.id,{'statef':'Refused'})
        for m in self.pool.get('balance.scorecard.customer').browse(cr,uid,search_valuec):
            self.pool.get('balance.scorecard.customer').write(cr,uid,m.id,{'statef':'Refused'})
        for m in self.pool.get('balance.scorecard.internal').browse(cr,uid,search_valuei):
            self.pool.get('balance.scorecard.internal').write(cr,uid,m.id,{'statef':'Refused'})
        for m in self.pool.get('balance.scorecard.learning').browse(cr,uid,search_valuel):
            self.pool.get('balance.scorecard.learning').write(cr,uid,m.id,{'statef':'Refused'})
        if specify_reason_for_refusal == False:
            raise osv.except_osv(_('Warning!'),_("Please specify a reason for refusal. Click on the checkbox for 'Specify reason for refusal of KRA'"))
        elif not reason_for_refusal:
            raise osv.except_osv(_('Warning!'),_("Please specify a reason for refusal of KRA"))
        else:
            return self.write(cr, uid, ids, {'state': 'Refused'}, context=context)

    #Function when KRA record is set to Draft
    def set_draft(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        form_id = x.id
        search_valuef = self.pool.get('balance.scorecard.financial').search(cr,uid,[('financial_id','=',form_id)])
        search_valuec = self.pool.get('balance.scorecard.customer').search(cr,uid,[('cust_id','=',form_id)])
        search_valuei = self.pool.get('balance.scorecard.internal').search(cr,uid,[('internal_id','=',form_id)])
        search_valuel = self.pool.get('balance.scorecard.learning').search(cr,uid,[('learning_id','=',form_id)])
        for m in self.pool.get('balance.scorecard.financial').browse(cr,uid,search_valuef):
            self.pool.get('balance.scorecard.financial').write(cr,uid,m.id,{'statef':'New'})
        for m in self.pool.get('balance.scorecard.customer').browse(cr,uid,search_valuec):
            self.pool.get('balance.scorecard.customer').write(cr,uid,m.id,{'statef':'New'})
        for m in self.pool.get('balance.scorecard.internal').browse(cr,uid,search_valuei):
            self.pool.get('balance.scorecard.internal').write(cr,uid,m.id,{'statef':'New'})
        for m in self.pool.get('balance.scorecard.learning').browse(cr,uid,search_valuel):
            self.pool.get('balance.scorecard.learning').write(cr,uid,m.id,{'statef':'New'})
                
        return self.write(cr, uid, ids, { 'state': 'New'}, context=context)
 

    #Print Employee Balance Scorecard in an Excel format.
    def export_excel(self,cr,uid,ids,context):
        list_left = []
        list_right = []
        for h in self.browse(cr, uid, ids, context=None):
            formid = h.id
            descr = h.name
            emp_name = h.emp_name.name
            depart = h.department.name            
            emp_code = h.emp_code
            join_date = (h.join_date)
            join_date = datetime.strptime(join_date, "%Y-%m-%d").strftime("%d-%m-%Y")
            job = h.job.name
            manager_id = h.manager_id.name
            appraisal_year = h.appraisal_year.name
            weightage_financial = h.weightage_financial
            weightage_financial = str(weightage_financial)+'%'
            weightage_customer = h.weightage_customer
            weightage_customer = str(weightage_customer)+'%'
            weightage_internal = h.weightage_internal
            weightage_internal = str(weightage_internal)+'%'
            weightage_learning = h.weightage_learning
            weightage_learning = str(weightage_learning)+'%'
            total_weightage = h.total_weightage
            total_weightage = str(total_weightage)+'%'
            total_self_rating = h.total_self_rating
            total_app_rating = h.total_app_rating
            total_mgmt_rating = h.total_mgmt_rating
            total_score = h.total_score
            list_left.append(['Description', descr])
            list_left.append(['Employee Name', emp_name])
            list_left.append(['Designation', job]) 
            list_left.append(['Join Date', join_date]) 
            list_right.append(['Employee Code', emp_code])
            list_right.append(['Department', depart])
            list_right.append(['Reporting To', manager_id])
            list_right.append(['Appraisal Year', appraisal_year])
        print 'in the Excel export'
        path_obj = self.pool.get('export.table.config')
        path_ids = path_obj.search(cr, uid, [])
        directory = path_obj.browse(cr, uid, path_ids[0]).path
        table_name = '.Employee Balance Scorecard'
        new_file = '%s %s.xlsx'%(table_name,emp_name)
        print new_file
        full_path = directory+'/'+new_file
        print full_path
        workbook = xlsxwriter.Workbook(full_path)
        workbook = xlsxwriter.Workbook(full_path)
        worksheet = workbook.add_worksheet()
        format1 = workbook.add_format()
        cell_format = workbook.add_format({'bold': True, 'font_color': 'black'})
        print workbook,'workbooook'
        # Some data we want to write to the worksheet.
        text_wrap = workbook.add_format({'text_wrap': 1, 'valign': 'top'})
        text_wrap.set_border(style=2)
        # Start from the first cell. Rows and columns are zero indexed.
        format_border = workbook.add_format({'bold': True, 'font_color': 'black'})
        format_border.set_border(style=2)
        format_border.set_align('center')
        format_border.set_align('vcenter')
        cell_format.set_border(style=2)
        row = 2
        col = 0        
        search_valuef = self.pool.get('balance.scorecard.financial').search(cr,uid,[('financial_id','=',formid)])
        search_valuec = self.pool.get('balance.scorecard.customer').search(cr,uid,[('cust_id','=',formid)])
        search_valuei = self.pool.get('balance.scorecard.internal').search(cr,uid,[('internal_id','=',formid)])
        search_valuel = self.pool.get('balance.scorecard.learning').search(cr,uid,[('learning_id','=',formid)])
        
        financial_count =[]
        financial_kra = []
        financial_pm = []
        financial_wt = []
        financial_sr = []
        financial_ar = []
        financial_mr = []
        financial_fs = []
        financial_act = []
        financial_com = []
        count = 0
        for m in self.pool.get('balance.scorecard.financial').browse(cr,uid,search_valuef):
            kra = m.KRA
            performance_measure = m.performance_measure
            weightage = m.weightage
            weightage = str(weightage) +'%'
            self_rating = m.self_rating
            app_rating = m.app_rating
            mgmt_rating = m.mgmt_rating
            weighted_scoref = m.weighted_scoref
            if m.action_plan:
                action_plan = m.action_plan
            else:
                action_plan = ''
            if m.comments:
                comments = m.comments
            else:
                comments = ''
            count+=1
            financial_count.append(count)
            financial_kra.append(kra)
            financial_pm.append(performance_measure)
            financial_wt.append(weightage)
            financial_sr.append(self_rating)
            financial_ar.append(app_rating)
            financial_mr.append(mgmt_rating)
            financial_fs.append(weighted_scoref)
            financial_act.append(action_plan)
            financial_com.append(comments)
        print financial_count, financial_kra, financial_pm, financial_wt

        customer_count =[]
        customer_kra = []
        customer_pm = []
        customer_wt = []
        customer_sr = []
        customer_ar = []
        customer_mr = []
        customer_cs = []
        customer_act = []
        customer_com = []
        count1 = 0
        for m in self.pool.get('balance.scorecard.customer').browse(cr,uid,search_valuec):
            kra = m.KRA
            performance_measure = m.performance_measure
            weightage = m.weightage
            weightage = str(weightage) +'%'
            self_rating = m.self_rating
            app_rating = m.app_rating
            mgmt_rating = m.mgmt_rating
            weighted_scorec = m.weighted_scorec
            if m.action_plan:
                action_plan = m.action_plan
            else:
                action_plan = ''
            if m.comments:
                comments = m.comments
            else:
                comments = ''
            count1+=1
            customer_count.append(count1)
            customer_kra.append(kra)
            customer_pm.append(performance_measure)
            customer_wt.append(weightage)
            customer_sr.append(self_rating)
            customer_ar.append(app_rating)
            customer_mr.append(mgmt_rating)
            customer_cs.append(weighted_scorec)
            customer_act.append(action_plan)
            customer_com.append(comments)
        #print customer_count, customer_kra, customer_pm, customer_wt

        internal_count =[]
        internal_kra = []
        internal_pm = []
        internal_wt = []
        internal_sr = []
        internal_ar = []
        internal_mr = []
        internal_is = []
        internal_act = []
        internal_com = []
        count2 = 0
        for m in self.pool.get('balance.scorecard.internal').browse(cr,uid,search_valuei):
            kra = m.KRA
            performance_measure = m.performance_measure
            weightage = m.weightage
            weightage = str(weightage) +'%'
            self_rating = m.self_rating
            app_rating = m.app_rating
            mgmt_rating = m.mgmt_rating
            weighted_scorei = m.weighted_scorei
            if m.action_plan:
                action_plan = m.action_plan
            else:
                action_plan = ''
            if m.comments:
                comments = m.comments
            else:
                comments = ''
            count2+=1
            internal_count.append(count2)
            internal_kra.append(kra)
            internal_pm.append(performance_measure)
            internal_wt.append(weightage)
            internal_sr.append(self_rating)
            internal_ar.append(app_rating)
            internal_mr.append(mgmt_rating)
            internal_is.append(weighted_scorei)
            internal_act.append(action_plan)
            internal_com.append(comments)
        print internal_count, internal_kra, internal_pm, internal_wt


        learning_count =[]
        learning_kra = []
        learning_pm = []
        learning_wt = []
        learning_sr = []
        learning_ar = []
        learning_mr = []
        learning_ls = []
        learning_act = []
        learning_com = []
        count3 = 0
        for m in self.pool.get('balance.scorecard.learning').browse(cr,uid,search_valuel):
            kra = m.KRA
            performance_measure = m.performance_measure
            weightage = m.weightage
            weightage = str(weightage) +'%'
            self_rating = m.self_rating
            app_rating = m.app_rating
            mgmt_rating = m.mgmt_rating
            weighted_scorel = m.weighted_scorel
            if m.action_plan:
                action_plan = m.action_plan
            else:
                action_plan = ''
            if m.comments:
                comments = m.comments
            else:
                comments = ''
            count3+=1
            learning_count.append(count3)
            learning_kra.append(kra)
            learning_pm.append(performance_measure)
            learning_wt.append(weightage)
            learning_sr.append(self_rating)
            learning_ar.append(app_rating)
            learning_mr.append(mgmt_rating)
            learning_ls.append(weighted_scorel)
            learning_act.append(action_plan)
            learning_com.append(comments)
        print learning_count, learning_kra, learning_pm, learning_wt

        worksheet.set_row(0,50,cell_format)
        worksheet.set_column(0,10,40,cell_format)
        worksheet.write(0,0,'Balance Score Card')
        
        # Iterate over the data and write it out row by row.
        
        
        for item, cost in (list_left):            
            worksheet.write(row, col,     item,format_border )
            worksheet.write(row, col + 1, cost,format_border)
            row += 1
        row1 = 2
        col1 = 0
        for item, cost in (list_right):
            worksheet.write(row1 ,  col1 + 3 ,   item,format_border)
            worksheet.write(row1, col1 + 4 , cost,format_border)
            row1 += 1
        row2 = 7
        col2 = 0
        
        worksheet.set_row(7,30,cell_format)
        
        format = workbook.add_format({'bold': True, 'font_color': 'black'})
        format.set_pattern(1)  # This is optional when using a solid fill.
        format.set_bg_color('yellow')
        format.set_align('center')
        format.set_align('vcenter')
        format.set_border(style=2)
        format_wrap = workbook.add_format()
        format_wrap.set_text_wrap()
        format_wrap.set_border(style=2)
        format3 = workbook.add_format({'bold': True, 'font_color': 'black'})
        format3.set_rotation(90)
        format3.set_bg_color('#66CC99')
        format3.set_align('center')
        format3.set_align('vcenter')
        format3.set_border(style=2)
        header = ['Sr. No.', 'KRA (As identified for corresponding period)', 'Performance Measure', 'Weightage 100%',  'Self Rating', 'Appraiser Rating (R) on a scale of 5', 'Management Rating (R) on a scale of 5','Weighted Score W*R=Total Score', 'Action Plan for KRA', 'Comments']
        for item in (header):
            worksheet.write(row2 ,  col2 ,   item, format)
            col2 += 1
        worksheet.write(8 ,  1 ,   'Financial', format)
        worksheet.write(8 ,  3 ,   weightage_financial, format)
        row3 = 9
        col3 = 0
        col4 = 1
        col5 = 2
        col6 = 3
        col7 = 4
        col8 = 5
        col9 = 6
        col10 = 7
        col11 = 8
        col12 = 9
        row_range=[]
        for item1, item2, item3, item4, item5, item6, item7, item8, item9 in zip(financial_kra, financial_pm, financial_wt, financial_sr, financial_ar, financial_mr, financial_fs, financial_act, financial_com):
            worksheet.write(row3 ,  col4 ,   item1, format_wrap)
            worksheet.write(row3 ,  col5 ,   item2, format_wrap)
            worksheet.write(row3 ,  col6 ,   item3, format_border)
            worksheet.write(row3 ,  col7 ,   item4, format_border)
            worksheet.write(row3 ,  col8 ,   item5, format_border)
            worksheet.write(row3 ,  col9 ,   item6, format_border)
            worksheet.write(row3 ,  col10 ,   item7, format_border)
            worksheet.write(row3 ,  col11 ,   item8, format_wrap)
            worksheet.write(row3 ,  col12 ,   item9, format_wrap)
            worksheet.set_row(row3, 50,cell_format)
            row3 += 1
            row_range.append(row3)
        if len(row_range) >=2:    
            merge_row = 'A'+str(row_range[0])+':'+'A'+str(row_range[-1:][0])
        else:
            merge_row = 'A'+str(row_range[0])+':'+'A'+str(row_range[0])
        print merge_row
        worksheet.merge_range(merge_row, '1.Financial', format3)
        print row3, row_range, col6, 'value of row3'
        row4 = row3+1
        worksheet.write(row4 ,  1 ,   'Customer', format)
        worksheet.write(row4 ,  3 ,   weightage_customer, format)
        row5 = row4+1
        row_range=[]
        for item1, item2, item3, item4, item5, item6, item7, item8, item9 in zip(customer_kra, customer_pm, customer_wt, customer_sr, customer_ar, customer_mr, customer_cs, customer_act, customer_com):
            worksheet.write(row5 ,  col4 ,   item1, format_wrap)
            worksheet.write(row5 ,  col5 ,   item2, format_wrap)
            worksheet.write(row5 ,  col6 ,   item3, format_border)
            worksheet.write(row5 ,  col7 ,   item4, format_border)
            worksheet.write(row5 ,  col8 ,   item5, format_border)
            worksheet.write(row5 ,  col9 ,   item6, format_border)
            worksheet.write(row5 ,  col10 ,   item7, format_border)
            worksheet.write(row5 ,  col11 ,   item8, format_wrap)
            worksheet.write(row5 ,  col12 ,   item9, format_wrap)
            worksheet.set_row(row5, 50,cell_format)
            row5 += 1
            row_range.append(row5)
        if row_range:
            if len(row_range) >=2:
                merge_row = 'A'+str(row_range[0])+':'+'A'+str(row_range[-1:][0])
            else:
                merge_row = 'A'+str(row_range[0])+':'+'A'+str(row_range[0])
        print merge_row
        worksheet.merge_range(merge_row, '2.Customer', format3)
        print row5, col6, 'value of row5'
        row6 = row5+1
        worksheet.write(row6 ,  1 ,   'Internal Process', format)
        worksheet.write(row6 ,  3 ,   weightage_internal, format)
        row7 = row6+1
        row_range=[]
        for item1, item2, item3, item4, item5, item6, item7, item8, item9 in zip( internal_kra, internal_pm, internal_wt, internal_sr, internal_ar, internal_mr, internal_is, internal_act, internal_com):
            worksheet.write(row7 ,  col4 ,   item1, format_wrap)
            worksheet.write(row7 ,  col5 ,   item2, format_wrap)
            worksheet.write(row7 ,  col6 ,   item3, format_border)
            worksheet.write(row7 ,  col7 ,   item4, format_border)
            worksheet.write(row7 ,  col8 ,   item5, format_border)
            worksheet.write(row7 ,  col9 ,   item6, format_border)
            worksheet.write(row7 ,  col10 ,   item7, format_border)
            worksheet.write(row7 ,  col11 ,   item8, format_wrap)
            worksheet.write(row7 ,  col12 ,   item9, format_wrap)
            worksheet.set_row(row7, 50,cell_format)
            row7 += 1
            row_range.append(row7)
        if row_range:
            if len(row_range) >=2:    
                merge_row = 'A'+str(row_range[0])+':'+'A'+str(row_range[-1:][0])
            else:
                merge_row = 'A'+str(row_range[0])+':'+'A'+str(row_range[0])
        print merge_row
        worksheet.merge_range(merge_row, '3.Internal Process', format3)
        print row7, col6, 'value of row7'
        row8 = row7+1
        worksheet.write(row8 ,  1 ,   'Learning & Growth', format)
        worksheet.write(row8 ,  3 ,   weightage_learning, format)
        row9 = row8+1
        row_range=[]
        for item1, item2, item3, item4, item5, item6, item7, item8, item9 in zip(learning_kra, learning_pm, learning_wt, learning_sr, learning_ar, learning_mr, learning_ls, learning_act, learning_com):
            worksheet.write(row9 ,  col4 ,   item1, format_wrap)
            worksheet.write(row9 ,  col5 ,   item2, format_wrap)
            worksheet.write(row9 ,  col6 ,   item3, format_border)
            worksheet.write(row9 ,  col7 ,   item4, format_border)
            worksheet.write(row9 ,  col8 ,   item5, format_border)
            worksheet.write(row9 ,  col9 ,   item6, format_border)
            worksheet.write(row9 ,  col10 ,   item7, format_border)
            worksheet.write(row9 ,  col11 ,   item8, format_wrap)
            worksheet.write(row9 ,  col12 ,   item9, format_wrap)
            worksheet.set_row(row9, 50,cell_format)
            row9 += 1
            row_range.append(row9)
        if row_range:
            if len(row_range) >=2:    
                merge_row = 'A'+str(row_range[0])+':'+'A'+str(row_range[-1:][0])
            else:
                merge_row = 'A'+str(row_range[0])+':'+'A'+str(row_range[0])
        print merge_row
        worksheet.merge_range(merge_row, '4.Learning & Growth', format3)
        row10 = row9+1
        worksheet.write(row10 ,  1 ,   'Total Score (Appraiser Rating)-KRAs', format)
        worksheet.write(row10 ,  3 ,   total_weightage, format)
        worksheet.write(row10 ,  4 ,   total_self_rating, format_border)
        worksheet.write(row10 ,  5 ,   total_app_rating, format_border)
        worksheet.write(row10 ,  6 ,   total_mgmt_rating, format_border)
        worksheet.write(row10 ,  7 ,   total_score, format_border)

        row11 = row10+1
        worksheet.write(row11 ,  1 ,   'Signature Employee:', format_border)
        worksheet.write(row11 ,  8 ,   'Signature Appraiser:', format_border)
        worksheet.write(row11+1 ,  1 ,   'Date:', format_border)
        worksheet.write(row11+1 ,  8 ,   'Date:', format_border)
        workbook.close()
        self.write(cr, uid, ids, {'file_url':full_path,'file_name':new_file})
        value_record = self._retrieve_file(cr, uid, ids, name='export_file',value=None,arg=None,context=None)
    
class balance_scorecard_financial(osv.osv):
    _name = "balance.scorecard.financial"
    _rec_name = 'KRA' 
    _description = "Employee Balance Scorecard Financial"
        
    # def _calculate_weighted_score(self, cr, uid, ids, field_name, arg, context=None):
    #     if not ids:
    #         return {}
    #     for j in self.browse(cr, uid, ids, context=context):
    #         mgmt_rating = j.mgmt_rating
    #         if mgmt_rating:
    #             cr.execute("SELECT l.id,COALESCE((l.weightage/100) * l.mgmt_rating,0) AS weighted_score FROM balance_scorecard_financial l WHERE id IN %s GROUP BY l.id ",(tuple(ids),))
    #         else:
    #             cr.execute("SELECT l.id,COALESCE((l.weightage/100) * l.app_rating,0) AS weighted_score FROM balance_scorecard_financial l WHERE id IN %s GROUP BY l.id ",(tuple(ids),))
    #     res = dict(cr.fetchall())
    #     return res   
    
    def _calculate_weighted_score(self, cr, uid, ids, field_name, arg, context=None):
        res ={}
        print ids
        if context is None:
            context = {}
        for j in self.browse(cr, uid, ids, context=context):
            total = 0.0
            mgmt_rating = j.mgmt_rating
            app_rating = j.app_rating
            weightage = j.weightage
            if mgmt_rating:
                total = total + (weightage/100) * mgmt_rating
            elif app_rating:
                total = total + (weightage/100) * app_rating
            else:
                total = 0.0
            res[j.id] = total
        return res

    _columns = {
        'financial_id': fields.many2one('employee.balance.scorecard', 'Financial'),
        'sr_no': fields.char('Sr.No.'),
        'KRA':fields.char('KRA (As identified for corresponding period)',),
        'performance_measure':fields.char('Performance Measure'),
        'weightage':fields.float('Weightage (W in %)'),
        'self_rating': fields.float('Self Rating [on a scale of 1 to 5]'),
        'app_rating': fields.float('Appraiser Rating(R) [on a scale of 1 to 5]'),
        'mgmt_rating': fields.float('Mgmt Rating(R) [on a scale of 1 to 5]'),
        'weighted_scoref': fields.function(_calculate_weighted_score, string='Weighted Score (W*R = Total Score)',store=True),
        'type': fields.char('Type', readonly=True),
        # 'flag': fields.boolean('Flag')
        'statef': fields.selection([('New', 'New'),('Waiting for Self Rate','Waiting for Self Rating'),('Self Rating Given','Employee Self Rating'),('Submitted To Manager', 'Submitted To Manager'),('Waiting Manager Approval', "Manager's Rating"),('Submitted To Mgmt', 'Submitted To Mgmt'),('Reviewed By Mgmt', 'Reviewed By Mgmt'),('Publish','Published'),('Appraisal Meeting','Appraisal Meeting'),('Refused','Refused')], 'Status'),
        'action_plan': fields.text('Action Plan for KRA'),
        'comments': fields.text('Comments'),
        'active': fields.boolean('Active')
    }
    
    _defaults = {  
        'type': 'Financial',
        'statef': 'New',
        'active': True
        } 
    
    
    def onchange_self_rating(self, cr, uid, ids, self_rating):
   
        if self_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
            raise osv.except_osv(_('Warning!'),_('In Financial Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the self rating column'))
        return False    
    
    def onchange_app_rating(self, cr, uid, ids, app_rating):
       
        if app_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
            raise osv.except_osv(_('Warning!'),_('In Financial Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the self rating column'))     
        return False   
    
    def onchange_mgmt_rating(self, cr, uid, ids, mgmt_rating):
       
        if mgmt_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
            raise osv.except_osv(_('Warning!'),_('In Financial Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the self rating column'))     
        return False 
    
class balance_scorecard_customer(osv.osv):
    _name = "balance.scorecard.customer"
    _rec_name = 'KRA'
    _description = "Employee Balance Scorecard Customer"
    
    # def _calculate_weighted_score(self, cr, uid, ids, field_name, arg, context=None):
    #     if not ids:
    #         return {}
    #     for j in self.browse(cr, uid, ids, context=context):
    #         mgmt_rating = j.mgmt_rating
    #         if mgmt_rating:
    #             cr.execute("SELECT l.id,COALESCE((l.weightage/100) * l.mgmt_rating,0) AS weighted_score FROM balance_scorecard_customer l WHERE id IN %s GROUP BY l.id ",(tuple(ids),))
    #         else:
    #             cr.execute("SELECT l.id,COALESCE((l.weightage/100) * l.app_rating,0) AS weighted_score FROM balance_scorecard_customer l WHERE id IN %s GROUP BY l.id ",(tuple(ids),))
    #     res = dict(cr.fetchall())
    #     return res

    def _calculate_weighted_score(self, cr, uid, ids, field_name, arg, context=None):
        res ={}
        print ids
        if context is None:
            context = {}
        for j in self.browse(cr, uid, ids, context=context):
            total = 0.0
            mgmt_rating = j.mgmt_rating
            app_rating = j.app_rating
            weightage = j.weightage
            if mgmt_rating:
                total = total + (weightage/100) * mgmt_rating
            elif app_rating:
                total = total + (weightage/100) * app_rating
            else:
                total = 0.0
            res[j.id] = total
        return res
    
    _columns = {
        'cust_id': fields.many2one('employee.balance.scorecard', 'Customer'),
        'sr_no': fields.char('Sr.No.'),
        'KRA':fields.char('KRA (As identified for corresponding period)'),
        'performance_measure':fields.char('Performance Measure'),
        'weightage':fields.float('Weightage (W in %)'),
        'self_rating': fields.float('Self Rating [on a scale of 1 to 5]'),
        'app_rating': fields.float('Appraiser Rating(R) [on a scale of 1 to 5]'),
        'mgmt_rating': fields.float('Mgmt Rating(R) [on a scale of 1 to 5]'),
        'weighted_scorec': fields.function(_calculate_weighted_score, string='Weighted Score (W*R = Total Score)',store=True),
        'type': fields.char('Type', readonly=True),
        'statef': fields.selection([('New', 'New'),('Waiting for Self Rate','Waiting for Self Rating'),('Self Rating Given','Employee Self Rating'),('Submitted To Manager', 'Submitted To Manager'),('Waiting Manager Approval', "Manager's Rating"),('Submitted To Mgmt', 'Submitted To Mgmt'),('Reviewed By Mgmt', 'Reviewed By Mgmt'),('Appraisal Meeting','Appraisal Meeting'),('Publish','Published'),('Refused','Refused')], 'Status'),
        'action_plan': fields.text('Action Plan for KRA'),
        'comments': fields.text('Comments'),
        'active': fields.boolean('Active')
    }
    
    _defaults = {  
        'type': 'Customer',
        'statef': 'New',
        'active':True
        } 
    
    def onchange_self_rating(self, cr, uid, ids, self_rating):
   
        if self_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
            raise osv.except_osv(_('Warning!'),_('In Customer Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the self rating column'))
        return False    
    
    def onchange_app_rating(self, cr, uid, ids, app_rating):
       
        if app_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
            raise osv.except_osv(_('Warning!'),_('In Customer Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the self rating column'))     
        return False 

    def onchange_mgmt_rating(self, cr, uid, ids, mgmt_rating):
       
        if mgmt_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
            raise osv.except_osv(_('Warning!'),_('In Customer Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5 in the self rating column'))     
        return False   
    
class balance_scorecard_internal(osv.osv):
    _name = "balance.scorecard.internal"
    _rec_name = 'KRA'
    _description = "Employee Balance Scorecard Internal"
    
    # def _calculate_weighted_score(self, cr, uid, ids, field_name, arg, context=None):
    #     if not ids:
    #         return {}
    #     for j in self.browse(cr, uid, ids, context=context):
    #         mgmt_rating = j.mgmt_rating
    #         if mgmt_rating:
    #             cr.execute("SELECT l.id,COALESCE((l.weightage/100) * l.mgmt_rating,0) AS weighted_score FROM balance_scorecard_internal l WHERE id IN %s GROUP BY l.id ",(tuple(ids),))
    #         else:
    #             cr.execute("SELECT l.id,COALESCE((l.weightage/100) * l.app_rating,0) AS weighted_score FROM balance_scorecard_internal l WHERE id IN %s GROUP BY l.id ",(tuple(ids),))
    #     res = dict(cr.fetchall())
    #     return res

    def _calculate_weighted_score(self, cr, uid, ids, field_name, arg, context=None):
        res ={}
        print ids
        if context is None:
            context = {}
        for j in self.browse(cr, uid, ids, context=context):
            total = 0.0
            mgmt_rating = j.mgmt_rating
            app_rating = j.app_rating
            weightage = j.weightage
            if mgmt_rating:
                total = total + (weightage/100) * mgmt_rating
            elif app_rating:
                total = total + (weightage/100) * app_rating
            else:
                total = 0.0
            res[j.id] = total
        return res
    
    _columns = {
        'internal_id': fields.many2one('employee.balance.scorecard', 'Internal Process'),
        'sr_no': fields.char('Sr.No.'),
        'KRA':fields.char('KRA (As identified for corresponding period)'),
        'performance_measure':fields.char('Performance Measure'),
        'weightage':fields.float('Weightage (W in %)'),
        'self_rating': fields.float('Self Rating [on a scale of 1 to 5]'),
        'app_rating': fields.float('Appraiser Rating(R) [on a scale of 1 to 5]'),
        'mgmt_rating': fields.float('Mgmt Rating(R) [on a scale of 1 to 5]'),
        'weighted_scorei': fields.function(_calculate_weighted_score, string='Weighted Score (W*R = Total Score)',store=True),
        'type': fields.char('Type', readonly=True),
        'statef': fields.selection([('New', 'New'),('Waiting for Self Rate','Waiting for Self Rating'),('Self Rating Given','Employee Self Rating'),('Submitted To Manager', 'Submitted To Manager'),('Waiting Manager Approval', "Manager's Rating"),('Submitted To Mgmt', 'Submitted To Mgmt'),('Reviewed By Mgmt', 'Reviewed By Mgmt'),('Appraisal Meeting','Appraisal Meeting'),('Publish','Published'),('Refused','Refused')], 'Status'),
        'action_plan': fields.text('Action Plan for KRA'),
        'comments': fields.text('Comments'),
        'active': fields.boolean('Active')
    }
    
    _defaults = {  
        'type': 'Internal Process',
        'statef': 'New',
        'active':True
        } 
    
    def onchange_self_rating(self, cr, uid, ids, self_rating):
   
        if self_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
            raise osv.except_osv(_('Warning!'),_('In Internal Process Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5'))
        return False    
    
    def onchange_app_rating(self, cr, uid, ids, app_rating):
       
        if app_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
            raise osv.except_osv(_('Warning!'),_('In Internal Process Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5'))     
        return False   

    def onchange_mgmt_rating(self, cr, uid, ids, mgmt_rating):
       
        if mgmt_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
            raise osv.except_osv(_('Warning!'),_('In Internal Process Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5'))     
        return False 
    
class balance_scorecard_learning(osv.osv):
    _name = "balance.scorecard.learning"
    _rec_name = 'KRA'
    _description = "Employee Balance Scorecard Learning"
    
    # def _calculate_weighted_score(self, cr, uid, ids, field_name, arg, context=None):
    #     if not ids:
    #         return {}
    #     for j in self.browse(cr, uid, ids, context=context):
    #         mgmt_rating = j.mgmt_rating
    #         if mgmt_rating:
    #             cr.execute("SELECT l.id,COALESCE((l.weightage/100) * l.mgmt_rating,0) AS weighted_score FROM balance_scorecard_learning l WHERE id IN %s GROUP BY l.id ",(tuple(ids),))
    #         else:
    #             cr.execute("SELECT l.id,COALESCE((l.weightage/100) * l.app_rating,0) AS weighted_score FROM balance_scorecard_learning l WHERE id IN %s GROUP BY l.id ",(tuple(ids),))
    #     res = dict(cr.fetchall())
    #     return res

    def _calculate_weighted_score(self, cr, uid, ids, field_name, arg, context=None):
        res ={}
        print ids
        if context is None:
            context = {}
        for j in self.browse(cr, uid, ids, context=context):
            total = 0.0
            mgmt_rating = j.mgmt_rating
            app_rating = j.app_rating
            weightage = j.weightage
            if mgmt_rating:
                total = total + (weightage/100) * mgmt_rating
            elif app_rating:
                total = total + (weightage/100) * app_rating
            else:
                total = 0.0
            res[j.id] = total
        return res
    
    _columns = {
        'learning_id': fields.many2one('employee.balance.scorecard', 'Learning & Growth'),
        'sr_no': fields.char('Sr.No.'),
        'KRA':fields.char('KRA (As identified for corresponding period)'),
        'performance_measure':fields.char('Performance Measure'),
        'weightage':fields.float('Weightage (W in %)'),
        'self_rating': fields.float('Self Rating [on a scale of 1 to 5]'),
        'app_rating': fields.float('Appraiser Rating(R) [on a scale of 1 to 5]'),
        'mgmt_rating': fields.float('Mgmt Rating(R) [on a scale of 1 to 5]'),
        'weighted_scorel': fields.function(_calculate_weighted_score, string='Weighted Score (W*R = Total Score)',store=True),
        'type': fields.char('Type', readonly=True),
        'statef': fields.selection([('New', 'New'),('Waiting for Self Rate','Waiting for Self Rating'),('Self Rating Given','Employee Self Rating'),('Submitted To Manager', 'Submitted To Manager'),('Waiting Manager Approval', "Manager's Rating"),('Submitted To Mgmt', 'Submitted To Mgmt'),('Reviewed By Mgmt', 'Reviewed By Mgmt'),('Appraisal Meeting','Appraisal Meeting'),('Publish','Published'),('Refused','Refused')], 'Status'),
        'action_plan': fields.text('Action Plan for KRA'),
        'comments': fields.text('Comments'),
        'active': fields.boolean('Active')
    } 
    
    _defaults = {  
        'type': 'Learning and Growth',
        'statef': 'New',
        'active': True
        }
    
    def onchange_self_rating(self, cr, uid, ids, self_rating):
   
        if self_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
            raise osv.except_osv(_('Warning!'),_('In Learning & Growth Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5'))
        return False    
    
    def onchange_app_rating(self, cr, uid, ids, app_rating):
       
        if app_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
            raise osv.except_osv(_('Warning!'),_('In Learning & Growth Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5'))     
        return False   
    
    def onchange_mgmt_rating(self, cr, uid, ids, mgmt_rating):
       
        if mgmt_rating not in (1,1.5,2,2.5,3,3.5,4,4.5,5):
            raise osv.except_osv(_('Warning!'),_('In Learning & Growth Section, Please rate on the Scale of 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5'))     
        return False 

class request_new_kra(osv.osv):
    _name = "request.new.kra"
    _description = "Request for New KRA"
    _inherit = 'mail.thread'
    
    def _employee_get(self, cr, uid, context=None):
        ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
        if ids:
            return ids[0]
        return False

    def _check_approval(self, cr, uid, ids, approved_var, field_names=None, arg=None, context=None):
        res ={}
        print ids
        if context is None:
            context = {}
        for j in self.browse(cr, uid, ids, context=context):
            print j.id
            res[j.id] = approved_var
            print approved_var, 'in fields.function'
        return res
    
    _columns = {
        'name': fields.char('Description'),
        'company_id': fields.many2one('res.company', 'Company'),
        'current_user':fields.many2one('res.users','Current User',size=32),
        'emp_name': fields.many2one('hr.employee', "Employee Name", required=True),
        'emp_code': fields.char('Employee Code'),
        'department': fields.many2one('hr.department', "Department", required=True),
        'join_date': fields.date("Date Of Joining"),
        'job': fields.many2one('hr.job', 'Designation'),
        'appraisal_year': fields.many2one('account.fiscalyear', 'Appraisal Year', required=True, select=True),
        'appraisal_cycle': fields.selection([('1','1'),('2','2'),('3','3'),('4','4')], 'Appraisal Cycle'),
        'state': fields.selection([('New', 'New'),('Submitted to Mgmt', 'Submitted to Manager'),('Escalated','Escalated'),('Approved', 'Approved By Manager'),('To be Refused','To be Refused'),('Refused', 'Refused')], 'Status'),    
        'kra_points_id': fields.one2many('kra.points','points_id', 'Add New KRA'),
        'change_kra_points_id': fields.one2many('kra.points.change','change_points_id', 'Change Existing KRA'),
        'note': fields.text('Note'),
        'manager_id': fields.many2one('hr.employee', 'Reporting To', required=True, domain="[('manager', '=', True)]"),
        'flag': fields.boolean('Flag'),
        'is_escalated': fields.boolean('Escalated'),
        'partial_approval': fields.boolean('Partial Approval'),
    }
    _defaults = {
        'state': 'New' ,
        'emp_name': _employee_get,
        'name': 'New KRA Request',
        'flag': False,
        'partial_approval':False
    }
    
    def onchange_kra_points_id(self,cr,uid,ids,kra_points_id):
        v={}
        kra_list =[]
        kar_yes_no_value = False
        for kra in kra_points_id:
            kra_yes_no = kra[2]
            if kra_yes_no:
                if kra_yes_no.has_key('yes_no'):
                    kar_yes_no_value = kra_yes_no.get('yes_no')
                kra_list.append(kar_yes_no_value)
        if 'Refused' in kra_list:
            v['partial_approval'] = True
        else:
            v['partial_approval'] = False
        return {'value':v}

    #Create function on request new/change existing kra process workflow
    def create(self, cr, uid, vals, context=None):
        line_values=[]
        add_kra_line_obj = self.pool.get('kra.points')
        change_kra_line = self.pool.get('kra.points.change')
        res_id = super(request_new_kra, self).create(cr, uid, vals, context=context)
        total_weightage_f, total_weightage_c, total_weightage_i, total_weightage_l = 0.0, 0.0, 0.0, 0.0
        weightage_add = 0.0
        weightage_change = 0.0
        kra_financial, kra_customer, kra_internal, kra_learning = 0.0, 0.0, 0.0, 0.0
        total_faw, total_caw, total_iaw, total_law = 0.0, 0.0, 0.0, 0.0
        total_fw, total_fchw, total_cw, total_cchw, total_iw, total_ichw, total_lw, total_lchw = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        print res_id
        print add_kra_line_obj, 'add kra line object'
        print change_kra_line, 'change kra line'
        if vals['kra_points_id']:
            print vals['kra_points_id']
            search_add_id = add_kra_line_obj.search(cr,uid,[('points_id','=',res_id)])
            print search_add_id, 'Adddddd IDDD'
            
            for main_form_id in add_kra_line_obj.browse(cr,uid,search_add_id):
                kra_type = main_form_id.type_of_kra
                if kra_type == 'Financial':
                    weightage_add = main_form_id.weightage                    
                    total_faw +=  weightage_add
                if kra_type == 'Customer':
                    weightage_add = main_form_id.weightage                    
                    total_caw +=  weightage_add
                if kra_type == 'Internal Process':
                    weightage_add = main_form_id.weightage                    
                    total_iaw +=  weightage_add
                if kra_type == 'Learning and Growth':
                    weightage_add = main_form_id.weightage                    
                    total_law +=  weightage_add
                    
        if vals['change_kra_points_id']:
            print vals['change_kra_points_id']
            search_change_id = change_kra_line.search(cr,uid,[('change_points_id','=',res_id)])
            
            for main_form_id in change_kra_line.browse(cr,uid,search_change_id):
                main_id = main_form_id.id
                action = main_form_id.action
                if not action:
                    raise osv.except_osv(_('Warning!'),_('Please select the type of action in the change in existing KRA table'))
                kraType = main_form_id.type_of_kra
                if action == 'Change':
                    if kraType == 'Financial':
                        changed_weightage = main_form_id.changed_weightage
                        kra_financial = main_form_id.KRA_financial.weightage
                        weightage_change = main_form_id.weightage
                        total_fw += weightage_change
                        total_fchw += changed_weightage
                        print weightage_change, kra_financial,'changeggggggggg'
                    if kraType == 'Customer':
                        changed_weightage = main_form_id.changed_weightage
                        kra_customer = main_form_id.KRA_customer.weightage
                        weightage_change = main_form_id.weightage
                        total_cw += weightage_change
                        total_cchw += changed_weightage
                        print weightage_change, kra_customer,'changeggggggggg'
                    if kraType == 'Internal Process':
                        changed_weightage = main_form_id.changed_weightage
                        kra_internal = main_form_id.KRA_internal.weightage
                        weightage_change = main_form_id.weightage
                        total_iw += weightage_change
                        total_ichw += changed_weightage
                        print weightage_change, kra_internal,'changeggggggggg'
                    if kraType == 'Learning and Growth':
                        changed_weightage = main_form_id.changed_weightage
                        kra_learning = main_form_id.KRA_learning.weightage
                        weightage_change = main_form_id.weightage
                        total_lw += weightage_change
                        total_lchw += changed_weightage
                        print weightage_change, kra_learning,'changeggggggggg'
        total_weightage_f = total_faw + total_fchw
        total_weightage_c = total_caw + total_cchw
        total_weightage_i = total_iaw + total_ichw
        total_weightage_l = total_law + total_lchw
        print total_weightage_f
        print total_faw
        # if action == 'Change' :
        #     if total_weightage_f != total_fw:
        #         raise osv.except_osv(_('Warning!'),_('The weightage for new KRA point and existing KRA should be %s in total')%(total_fw))
        #     if total_weightage_c != total_cw:
        #         raise osv.except_osv(_('Warning!'),_('The weightage for new KRA point and existing KRA should be %s in total')%(total_cw))
        #     if total_weightage_i != total_iw:
        #         raise osv.except_osv(_('Warning!'),_('The weightage for new KRA point and existing KRA should be %s in total')%(total_iw))    
        #     if total_weightage_l != total_lw:
        #         raise osv.except_osv(_('Warning!'),_('The weightage for new KRA point and existing KRA should be %s in total')%(total_lw))
        return res_id
        

    
    def onchange_employee(self, cr, uid, ids, emp_name, context=None):
        value = {'join_date': False,'department': False, 'job': False, 'emp_code': False,'manager_id': False,'appraisal_year':False }
        if emp_name:
            emp = self.pool.get('hr.employee').browse(cr, uid, emp_name)
            value['join_date'] = emp.join_date
            value['department'] = emp.department_id.id
            value['job'] = emp.job_id.id
            value['emp_code'] = emp.auto_emp_code
            value['manager_id'] = emp.parent_id.id
            today = datetime.today().date()
            yrs = self.pool.get('account.fiscalyear')
            if str(today)>='2015-04-01' and str(today)<='2016-03-31':
                search_add_id = yrs.search(cr,uid,[('name','=','2015-2016')])
                value['appraisal_year'] = search_add_id
            elif str(today)>='2016-04-01' and str(today)<='2017-03-31':
                search_add_id = yrs.search(cr,uid,[('name','=','2016-2017')])
                value['appraisal_year'] = search_add_id
            else:
                value['appraisal_year'] = ''
        return {'value': value}
    
    
    #Function for submitting the change/add KRA points
    def submit_request(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        add_points = x.kra_points_id
        change_points = x.change_kra_points_id
        form_id = x.id
        emp_name = x.emp_name.id
        appraisal_year = x.appraisal_year.id
        is_escalated = x.is_escalated
        res = self.pool.get('employee.balance.scorecard').search(cr, uid,[('emp_name', '=', emp_name),('appraisal_year','=',appraisal_year)], context=context)
        print res, 'resssss'
        for k in self.pool.get('employee.balance.scorecard').browse(cr,uid,res):
            form = k.id, 
            current_state = k.state
            financial = k.financial_kra_id
            customer = k.customer_kra_id
            internal = k.internal_kra_id
            learning = k.learning_kra_id
            total_weightage = k.weightage_financial
            print total_weightage, current_state, 'totallllll weightage and state' 
            if current_state not in ('New','Waiting for Self Rate'):
                raise osv.except_osv(_('Warning!'),_('You cannot request for adding a new KRA point as your KRA is already processed'))
        
        # if not add_points:
        #     raise osv.except_osv(_('Warning!'),_('Please Add a new KRA'))
        if add_points:
            if not change_points:
                raise osv.except_osv(_('Warning!'),_('You need to add a record in change existing KRA point'))
        
        if not change_points:
            raise osv.except_osv(_('Warning!'),_('You need to add a record in change existing KRA point'))
        add_kra_line_obj = self.pool.get('kra.points')
        change_kra_line = self.pool.get('kra.points.change')
        if not is_escalated:
            total_weightage_fc, total_weightage_cc, total_weightage_ic, total_weightage_lc = 0.0, 0.0, 0.0, 0.0
            total_weightage_fr, total_weightage_cr, total_weightage_ir, total_weightage_lr = 0.0, 0.0, 0.0, 0.0
            weightage_add = 0.0
            weightage_change = 0.0
            kra_financial, kra_customer, kra_internal, kra_learning = 0.0, 0.0, 0.0, 0.0
            print add_kra_line_obj, 'add kra line object'
            print change_kra_line, 'change kra line'
            total_faw, total_caw, total_iaw, total_law = 0.0, 0.0, 0.0, 0.0
            total_fwr, total_cwr, total_iwr, total_lwr = 0.0, 0.0, 0.0, 0.0
            total_fawr, total_cawr, total_iawr, total_lawr = 0.0, 0.0, 0.0, 0.0
            total_fw,total_fchw,total_cw,total_cchw,total_iw,total_ichw,total_lw,total_lchw = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
            
            if x.change_kra_points_id:            
                search_change_id = change_kra_line.search(cr,uid,[('change_points_id','=',x.id)])
                search_add_id = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id)])
                for main_form_id in change_kra_line.browse(cr,uid,search_change_id):
                    main_id = main_form_id.id
                    action = main_form_id.action
                    cw = main_form_id.changed_weightage 
                    sr_no_change = main_form_id.sr_no
                    search_change_sr_no_id = change_kra_line.search(cr,uid,[('change_points_id','=',x.id),('sr_no','=',sr_no_change)])
                    if search_change_sr_no_id:
                        if len(search_change_sr_no_id) > 1:
                            raise osv.except_osv(_('Warning!'),_('Record for serial no %s already exists in the change existing KRA point table. Please give proper serial nos.')%(sr_no_change))            
                    if not action:
                        raise osv.except_osv(_('Warning!'),_('Please select the type of action in the change in existing KRA table'))
                    if action == "Change":
                        if cw == 0.0:
                            raise osv.except_osv(_('Warning!'),_('In Change Existing KRA point table Changed Weightage can not be 0.0')) 
                    kraType = main_form_id.type_of_kra
                    if action == "Change":
                        if kraType == 'Financial':
                            kra_financial_weightage = main_form_id.KRA_financial.weightage
                            if main_form_id.weightage != kra_financial_weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Financial, you are not allowed to change the weightage in weightage column, you need to give the changed value in the Changed weightage column'))
                            search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Financial')])
                            print search_in_add
                            # if not search_in_add:
                            #    raise osv.except_osv(_('Warning!'),_('For type Financial & point no %s please add a record in Add new KRA point table.')%(sr_no_change))    
                            if search_in_add:
                                for f_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                        sr_no_add = f_id.sr_no
                                        f_wtg = f_id.weightage
                                        wtg = main_form_id.weightage
                                        cw = main_form_id.changed_weightage 
                                        print f_wtg ,'in financial'
                                        print total_fchw, 'total financial chnaged weightage in loop'
                                        total_fchw += f_wtg
                                if main_form_id.weightage != (cw + total_fchw):
                                    raise osv.except_osv(_('Warning!'),_('For type Financial and action change, the weightage for new KRA point and the changed weightage for existing KRA should be %s in total in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                            else:
                                for main_form_id in change_kra_line.browse(cr,uid,search_change_id):
                                    changed_weightage = main_form_id.changed_weightage
                                    weightage_change = main_form_id.weightage
                                    total_fw += weightage_change
                                    print total_fw
                                    total_fchw += changed_weightage
                                    print total_fchw
                                if total_fw != total_fchw:
                                    raise osv.except_osv(_('Warning!'),_('For type Financial and action change the weightage should be %s in total')%(total_fw))

                        if kraType == 'Customer':
                            kra_customer_weightage = main_form_id.KRA_customer.weightage
                            if main_form_id.weightage != kra_customer_weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Customer, you are not allowed to change the weightage in weightage column, you need to give the changed value in the Changed weightage column'))
                            search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Customer')])
                            # if not search_in_add:
                               # raise osv.except_osv(_('Warning!'),_('For type Customer & point no %s please add a record in Add new KRA point table.')%(sr_no_change))    
                            if search_in_add:
                                for c_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                        sr_no_add = c_id.sr_no
                                        c_wtg = c_id.weightage
                                        wtg = main_form_id.weightage
                                        cw = main_form_id.changed_weightage 
                                        total_cchw += c_wtg
                                if main_form_id.weightage != (cw + total_cchw):
                                    raise osv.except_osv(_('Warning!'),_('For type Customer and action change, the weightage for new KRA point and the changed weightage for existing KRA should be %s in total in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                            else:
                                for main_form_id in change_kra_line.browse(cr,uid,search_change_id):
                                    changed_weightage = main_form_id.changed_weightage
                                    weightage_change = main_form_id.weightage
                                    total_cw += weightage_change
                                    print total_cw
                                    total_cchw += changed_weightage
                                    print total_cchw
                                if total_cw != total_cchw:
                                    raise osv.except_osv(_('Warning!'),_('For type Customer and action change the weightage should be %s in total')%(total_cw))

                        if kraType == 'Internal Process':
                            kra_internal_weightage = main_form_id.KRA_internal.weightage
                            if main_form_id.weightage != kra_internal_weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Internal Process, you are not allowed to change the weightage in weightage column, you need to give the changed value in the Changed weightage column'))
                            search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Internal Process')])
                            # if not search_in_add:
                               # raise osv.except_osv(_('Warning!'),_('For type Internal Process & point no %s please add a record in Add new KRA point table.')%(sr_no_change))
                            if search_in_add:
                                for i_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                        sr_no_add = i_id.sr_no
                                        i_wtg = i_id.weightage
                                        wtg = main_form_id.weightage
                                        cw = main_form_id.changed_weightage 
                                        total_ichw += i_wtg
                                if main_form_id.weightage != (cw + total_ichw):
                                    raise osv.except_osv(_('Warning!'),_('For type Internal Process and action change, the weightage for new KRA point and the changed weightage for existing KRA should be %s in total in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                            else:
                                for main_form_id in change_kra_line.browse(cr,uid,search_change_id):
                                    changed_weightage = main_form_id.changed_weightage
                                    weightage_change = main_form_id.weightage
                                    total_iw += weightage_change
                                    print total_iw
                                    total_ichw += changed_weightage
                                    print total_ichw
                                if total_iw != total_ichw:
                                    raise osv.except_osv(_('Warning!'),_('For type Internal Process and action change the weightage should be %s in total')%(total_iw))

                        if kraType == 'Learning and Growth':
                            kra_learning_weightage = main_form_id.KRA_learning.weightage
                            if main_form_id.weightage != kra_learning_weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Learning and Growth, you are not allowed to change the weightage in weightage column, you need to give the changed value in the Changed weightage column'))
                            search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Learning and Growth')])
                            # if not search_in_add:
                               # raise osv.except_osv(_('Warning!'),_('For type Learning and Growth & point no %s please add a record in Add new KRA point table.')%(sr_no_change))
                            if search_in_add:
                                for l_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                        sr_no_add = l_id.sr_no
                                        l_wtg = l_id.weightage
                                        wtg = main_form_id.weightage
                                        cw = main_form_id.changed_weightage 
                                        total_lchw += l_wtg
                                if main_form_id.weightage != (cw + total_lchw):
                                    raise osv.except_osv(_('Warning!'),_('For type Learning and Growth, for action change, the weightage for new KRA point and the changed weightage for existing KRA should be %s in total in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                            else:
                                for main_form_id in change_kra_line.browse(cr,uid,search_change_id):
                                    changed_weightage = main_form_id.changed_weightage
                                    weightage_change = main_form_id.weightage
                                    total_lw += weightage_change
                                    print total_lw
                                    total_lchw += changed_weightage
                                    print total_lchw
                                if total_lw != total_lchw:
                                    raise osv.except_osv(_('Warning!'),_('For type Learning and Growth, for action change the weightage should be %s in total')%(total_iw))
                if action == "Replace":
                    if kraType == 'Financial':
                        kra_financial_weightage = main_form_id.KRA_financial.weightage
                        if main_form_id.weightage != kra_financial_weightage:
                            raise osv.except_osv(_('Warning!'),_('For type Financial, you are not allowed to change the weightage in weightage column'))
                        search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=',kraType),('type_of_kra','=','Financial')])
                        print search_in_add
                        if not search_in_add:
                            raise osv.except_osv(_('Warning!'),_('For type Financial & point no %s please add a record in Add new KRA point table.')%(sr_no_change))    
                        if search_in_add:
                            for f_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                sr_no_add = f_id.sr_no
                                f_wtg = f_id.weightage
                                total_fawr += f_wtg
                                if not sr_no_add or sr_no_add == 0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table, Reference to Point No. column cannot be empty'))
                                if f_wtg == 0.0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table Weightage can not be 0.0'))
                            if total_fawr != main_form_id.weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Financial and action Replace, the weightage for new KRA point should be equal to existing KRA point weightage i.e. %s in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                    if kraType == 'Customer':
                        kra_customer_weightage = main_form_id.KRA_customer.weightage
                        if main_form_id.weightage != kra_customer_weightage:
                            raise osv.except_osv(_('Warning!'),_('For type Customer, you are not allowed to change the weightage in weightage column.'))
                        search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Customer')])
                        print search_in_add
                        if not search_in_add:
                            raise osv.except_osv(_('Warning!'),_('For type Customer & point no %s please add a record in Add new KRA point table.')%(sr_no_change))    
                        if search_in_add:
                            for c_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                sr_no_add = c_id.sr_no
                                c_wtg = c_id.weightage
                                total_cawr += c_wtg
                                if not sr_no_add or sr_no_add == 0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table, Reference to Point No. column cannot be empty'))
                                if c_wtg == 0.0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table Weightage can not be 0.0'))
                            if total_cawr != main_form_id.weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Customer and action Replace, the weightage for new KRA point should be equal to existing KRA point weightage i.e. %s in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                    if kraType == 'Internal Process':
                        kra_internal_weightage = main_form_id.KRA_internal.weightage
                        if main_form_id.weightage != kra_internal_weightage:
                            raise osv.except_osv(_('Warning!'),_('For type Internal Process, you are not allowed to change the weightage in weightage column'))
                        search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Internal Process')])
                        print search_in_add
                        if not search_in_add:
                            raise osv.except_osv(_('Warning!'),_('For type Internal Process & point no %s please add a record in Add new KRA point table.')%(sr_no_change))    
                        if search_in_add:
                            for i_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                sr_no_add = i_id.sr_no
                                i_wtg = i_id.weightage
                                total_iawr += i_wtg
                                if not sr_no_add or sr_no_add == 0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table, Reference to Point No. column cannot be empty'))
                                if i_wtg == 0.0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table Weightage can not be 0.0'))
                            if total_iawr != main_form_id.weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Internal Process and action Replace, the weightage for new KRA point should be equal to existing KRA point weightage i.e. %s in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                    if kraType == 'Learning and Growth':
                        kra_learning_weightage = main_form_id.KRA_learning.weightage
                        if main_form_id.weightage != kra_learning_weightage:
                            raise osv.except_osv(_('Warning!'),_('For type Learning and Growth, you are not allowed to change the weightage in weightage column'))
                        search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Learning and Growth')])
                        print search_in_add
                        if not search_in_add:
                            raise osv.except_osv(_('Warning!'),_('For type Learning and Growth & point no %s please add a record in Add new KRA point table.')%(sr_no_change))    
                        if search_in_add:
                            for l_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                sr_no_add = l_id.sr_no
                                l_wtg = l_id.weightage
                                total_lawr += l_wtg
                                if not sr_no_add or sr_no_add == 0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table, Reference to Point No. column cannot be empty'))
                                if l_wtg == 0.0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table Weightage can not be 0.0'))
                            if total_lawr != main_form_id.weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Learning and Growth and action Replace, the weightage for new KRA point should be equal to existing KRA point weightage i.e. %s in reference to point no %s')%(main_form_id.weightage,sr_no_add))    

                for main_form_id in add_kra_line_obj.browse(cr,uid,search_add_id):
                    kra_type = main_form_id.type_of_kra
                    sr_no_add = main_form_id.sr_no
                    wtg = main_form_id.weightage
                    if not sr_no_add or sr_no_add == 0:
                        raise osv.except_osv(_('Warning!'),_('In Add New KRA point table, Reference to Point No. column cannot be empty'))
                    if wtg == 0.0:
                        raise osv.except_osv(_('Warning!'),_('In Add New KRA point table Weightage can not be 0.0'))
                    search_in_change_sr_no = change_kra_line.search(cr,uid,[('change_points_id','=',x.id),('sr_no','=',sr_no_add)])   
                    if not search_in_change_sr_no:
                        raise osv.except_osv(_('Warning!'),_('Record for reference to point no %s does no exist in the change existing KRA point table.')%(sr_no_add))              
                    if search_in_change_sr_no:
                        for m in change_kra_line.browse(cr,uid,search_in_change_sr_no):
                            typeOfKRA = m.type_of_kra
                            if typeOfKRA != kra_type:
                                raise osv.except_osv(_('Warning!'),_('For reference to point no %s the type does not match with the type of change existing kra point record')%(sr_no_add))  
                

        if is_escalated:
            total_weightage_fc, total_weightage_cc, total_weightage_ic, total_weightage_lc = 0.0, 0.0, 0.0, 0.0
            total_weightage_fr, total_weightage_cr, total_weightage_ir, total_weightage_lr = 0.0, 0.0, 0.0, 0.0
            weightage_add = 0.0
            weightage_change = 0.0
            kra_financial, kra_customer, kra_internal, kra_learning = 0.0, 0.0, 0.0, 0.0
            print add_kra_line_obj, 'add kra line object'
            print change_kra_line, 'change kra line'
            total_faw, total_caw, total_iaw, total_law = 0.0, 0.0, 0.0, 0.0
            total_fwr, total_cwr, total_iwr, total_lwr = 0.0, 0.0, 0.0, 0.0
            total_fawr, total_cawr, total_iawr, total_lawr = 0.0, 0.0, 0.0, 0.0
            total_fw,total_fchw,total_cw,total_cchw,total_iw,total_ichw,total_lw,total_lchw = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
            
            if x.change_kra_points_id:            
                search_change_id = change_kra_line.search(cr,uid,[('change_points_id','=',x.id)])
                search_add_id = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id)])
                for main_form_id in change_kra_line.browse(cr,uid,search_change_id):
                    main_id = main_form_id.id
                    action = main_form_id.action
                    cw = main_form_id.changed_weightage 
                    sr_no_change = main_form_id.sr_no
                    search_change_sr_no_id = change_kra_line.search(cr,uid,[('change_points_id','=',x.id),('sr_no','=',sr_no_change)])
                    if search_change_sr_no_id:
                        if len(search_change_sr_no_id) > 1:
                            raise osv.except_osv(_('Warning!'),_('Record for serial no %s already exists in the change existing KRA point table. Please give proper serial nos.')%(sr_no_change))            
                    if not action:
                        raise osv.except_osv(_('Warning!'),_('Please select the type of action in the change in existing KRA table'))
                    if action == "Change":
                        if cw == 0.0:
                            raise osv.except_osv(_('Warning!'),_('In Change Existing KRA point table Changed Weightage can not be 0.0')) 
                    kraType = main_form_id.type_of_kra
                    if action == "Change":
                        if kraType == 'Financial':
                            kra_financial_weightage = main_form_id.KRA_financial.weightage
                            if main_form_id.weightage != kra_financial_weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Financial, you are not allowed to change the weightage in weightage column, you need to give the changed value in the Changed weightage column'))
                            search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Financial')])
                            print search_in_add
                            if not search_in_add:
                               raise osv.except_osv(_('Warning!'),_('For type Financial & point no %s please add a record in Add new KRA point table.')%(sr_no_change))    
                            if search_in_add:
                                for f_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                        sr_no_add = f_id.sr_no
                                        f_wtg = f_id.weightage
                                        yes_no = f_id.yes_no
                                        wtg = main_form_id.weightage
                                        cw = main_form_id.changed_weightage 
                                        print f_wtg ,'in financial'
                                        print total_fchw, 'total financial chnaged weightage in loop'
                                        if yes_no =='Approved':
                                            total_fchw += f_wtg
                                if main_form_id.weightage != (cw + total_fchw):
                                    raise osv.except_osv(_('Warning!'),_('For type Financial and action change, the weightage for new Approved KRA point and the changed weightage for existing KRA should be %s in total in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                            # else:
                            #     for main_form_id in change_kra_line.browse(cr,uid,search_change_id):
                            #         changed_weightage = main_form_id.changed_weightage
                            #         weightage_change = main_form_id.weightage
                            #         total_fw += weightage_change
                            #         print total_fw
                            #         total_fchw += changed_weightage
                            #         print total_fchw
                            #     if total_fw != total_fchw:
                            #         raise osv.except_osv(_('Warning!'),_('For type Financial and action change the weightage should be %s in total')%(total_fw))

                        if kraType == 'Customer':
                            kra_customer_weightage = main_form_id.KRA_customer.weightage
                            if main_form_id.weightage != kra_customer_weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Customer, you are not allowed to change the weightage in weightage column, you need to give the changed value in the Changed weightage column'))
                            search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Customer')])
                            if not search_in_add:
                               raise osv.except_osv(_('Warning!'),_('For type Customer & point no %s please add a record in Add new KRA point table.')%(sr_no_change))    
                            if search_in_add:
                                for c_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                        sr_no_add = c_id.sr_no
                                        c_wtg = c_id.weightage
                                        yes_no = c_id.yes_no
                                        wtg = main_form_id.weightage
                                        cw = main_form_id.changed_weightage 
                                        if yes_no == 'Approved':
                                            total_cchw += c_wtg
                                if main_form_id.weightage != (cw + total_cchw):
                                    raise osv.except_osv(_('Warning!'),_('For type Customer and action change, the weightage for new Approved KRA point and the changed weightage for existing KRA should be %s in total in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                            # else:
                            #     for main_form_id in change_kra_line.browse(cr,uid,search_change_id):
                            #         changed_weightage = main_form_id.changed_weightage
                            #         weightage_change = main_form_id.weightage
                            #         total_cw += weightage_change
                            #         print total_cw
                            #         total_cchw += changed_weightage
                            #         print total_cchw
                            #     if total_cw != total_cchw:
                            #         raise osv.except_osv(_('Warning!'),_('For type Customer and action change the weightage should be %s in total')%(total_cw))

                        if kraType == 'Internal Process':
                            kra_internal_weightage = main_form_id.KRA_internal.weightage
                            if main_form_id.weightage != kra_internal_weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Internal Process, you are not allowed to change the weightage in weightage column, you need to give the changed value in the Changed weightage column'))
                            search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Internal Process')])
                            if not search_in_add:
                               raise osv.except_osv(_('Warning!'),_('For type Internal Process & point no %s please add a record in Add new KRA point table.')%(sr_no_change))
                            if search_in_add:
                                for i_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                        sr_no_add = i_id.sr_no
                                        i_wtg = i_id.weightage
                                        yes_no = i_id.yes_no
                                        wtg = main_form_id.weightage
                                        cw = main_form_id.changed_weightage 
                                        if yes_no == 'Approved':
                                            total_ichw += i_wtg
                                if main_form_id.weightage != (cw + total_ichw):
                                    raise osv.except_osv(_('Warning!'),_('For type Internal Process and action change, the weightage for new Approved KRA point and the changed weightage for existing KRA should be %s in total in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                            # else:
                            #     for main_form_id in change_kra_line.browse(cr,uid,search_change_id):
                            #         changed_weightage = main_form_id.changed_weightage
                            #         weightage_change = main_form_id.weightage
                            #         total_iw += weightage_change
                            #         print total_iw
                            #         total_ichw += changed_weightage
                            #         print total_ichw
                            #     if total_iw != total_ichw:
                            #         raise osv.except_osv(_('Warning!'),_('For type Internal Process and action change the weightage should be %s in total')%(total_iw))

                        if kraType == 'Learning and Growth':
                            kra_learning_weightage = main_form_id.KRA_learning.weightage
                            if main_form_id.weightage != kra_learning_weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Learning and Growth, you are not allowed to change the weightage in weightage column, you need to give the changed value in the Changed weightage column'))
                            search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Learning and Growth')])
                            if not search_in_add:
                               raise osv.except_osv(_('Warning!'),_('For type Learning and Growth & point no %s please add a record in Add new KRA point table.')%(sr_no_change))
                            if search_in_add:
                                for l_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                        sr_no_add = l_id.sr_no
                                        l_wtg = l_id.weightage
                                        yes_no = l_id.yes_no
                                        wtg = main_form_id.weightage
                                        cw = main_form_id.changed_weightage 
                                        if yes_no == 'Approved':
                                            total_lchw += l_wtg
                                if main_form_id.weightage != (cw + total_lchw):
                                    raise osv.except_osv(_('Warning!'),_('For type Learning and Growth, for action change, the weightage for new Approved KRA point and the changed weightage for existing KRA should be %s in total in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                            # else:
                            #     for main_form_id in change_kra_line.browse(cr,uid,search_change_id):
                            #         changed_weightage = main_form_id.changed_weightage
                            #         weightage_change = main_form_id.weightage
                            #         total_lw += weightage_change
                            #         print total_lw
                            #         total_lchw += changed_weightage
                            #         print total_lchw
                            #     if total_lw != total_lchw:
                            #         raise osv.except_osv(_('Warning!'),_('For type Learning and Growth, for action change the weightage should be %s in total')%(total_iw))
                if action == "Replace":
                    if kraType == 'Financial':
                        kra_financial_weightage = main_form_id.KRA_financial.weightage
                        if main_form_id.weightage != kra_financial_weightage:
                            raise osv.except_osv(_('Warning!'),_('For type Financial, you are not allowed to change the weightage in weightage column'))
                        search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=',kraType),('type_of_kra','=','Financial')])
                        print search_in_add
                        if not search_in_add:
                            raise osv.except_osv(_('Warning!'),_('For type Financial & point no %s please add a record in Add new KRA point table.')%(sr_no_change))    
                        if search_in_add:
                            for f_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                sr_no_add = f_id.sr_no
                                f_wtg = f_id.weightage
                                yes_no = f_id.yes_no
                                if yes_no == 'Approved':
                                    total_fawr += f_wtg
                                if not sr_no_add or sr_no_add == 0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table, Reference to Point No. column cannot be empty'))
                                if f_wtg == 0.0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table Weightage can not be 0.0'))
                            if total_fawr != main_form_id.weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Financial and action Replace, the weightage for new Approved KRA point should be equal to existing KRA point weightage i.e. %s in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                    if kraType == 'Customer':
                        kra_customer_weightage = main_form_id.KRA_customer.weightage
                        if main_form_id.weightage != kra_customer_weightage:
                            raise osv.except_osv(_('Warning!'),_('For type Customer, you are not allowed to change the weightage in weightage column.'))
                        search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Customer')])
                        print search_in_add
                        if not search_in_add:
                            raise osv.except_osv(_('Warning!'),_('For type Customer & point no %s please add a record in Add new KRA point table.')%(sr_no_change))    
                        if search_in_add:
                            for c_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                sr_no_add = c_id.sr_no
                                c_wtg = c_id.weightage
                                yes_no = c_id.yes_no
                                if yes_no == 'Approved':
                                    total_cawr += c_wtg
                                if not sr_no_add or sr_no_add == 0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table, Reference to Point No. column cannot be empty'))
                                if c_wtg == 0.0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table Weightage can not be 0.0'))
                            if total_cawr != main_form_id.weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Customer and action Replace, the weightage for new Approved KRA point should be equal to existing KRA point weightage i.e. %s in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                    if kraType == 'Internal Process':
                        kra_internal_weightage = main_form_id.KRA_internal.weightage
                        if main_form_id.weightage != kra_internal_weightage:
                            raise osv.except_osv(_('Warning!'),_('For type Internal Process, you are not allowed to change the weightage in weightage column'))
                        search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Internal Process')])
                        print search_in_add
                        if not search_in_add:
                            raise osv.except_osv(_('Warning!'),_('For type Internal Process & point no %s please add a record in Add new KRA point table.')%(sr_no_change))    
                        if search_in_add:
                            for i_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                sr_no_add = i_id.sr_no
                                i_wtg = i_id.weightage
                                yes_no = i_id.yes_no
                                if yes_no == 'Approved':
                                    total_iawr += i_wtg
                                if not sr_no_add or sr_no_add == 0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table, Reference to Point No. column cannot be empty'))
                                if i_wtg == 0.0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table Weightage can not be 0.0'))
                            if total_iawr != main_form_id.weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Internal Process and action Replace, the weightage for new Approved KRA point should be equal to existing KRA point weightage i.e. %s in reference to point no %s')%(main_form_id.weightage,sr_no_add))    
                    if kraType == 'Learning and Growth':
                        kra_learning_weightage = main_form_id.KRA_learning.weightage
                        if main_form_id.weightage != kra_learning_weightage:
                            raise osv.except_osv(_('Warning!'),_('For type Learning and Growth, you are not allowed to change the weightage in weightage column'))
                        search_in_add = add_kra_line_obj.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('type_of_kra','=','Learning and Growth')])
                        print search_in_add
                        if not search_in_add:
                            raise osv.except_osv(_('Warning!'),_('For type Learning and Growth & point no %s please add a record in Add new KRA point table.')%(sr_no_change))    
                        if search_in_add:
                            for l_id in add_kra_line_obj.browse(cr,uid,search_in_add):
                                sr_no_add = l_id.sr_no
                                l_wtg = l_id.weightage
                                yes_no = l_id.yes_no
                                if yes_no == 'Approved':
                                    total_lawr += l_wtg
                                if not sr_no_add or sr_no_add == 0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table, Reference to Point No. column cannot be empty'))
                                if l_wtg == 0.0:
                                    raise osv.except_osv(_('Warning!'),_('In Add New KRA point table Weightage can not be 0.0'))
                            if total_lawr != main_form_id.weightage:
                                raise osv.except_osv(_('Warning!'),_('For type Learning and Growth and action Replace, the weightage for new Approved KRA point should be equal to existing KRA point weightage i.e. %s in reference to point no %s')%(main_form_id.weightage,sr_no_add))    

                for main_form_id in add_kra_line_obj.browse(cr,uid,search_add_id):
                    kra_type = main_form_id.type_of_kra
                    sr_no_add = main_form_id.sr_no
                    wtg = main_form_id.weightage
                    if not sr_no_add or sr_no_add == 0:
                        raise osv.except_osv(_('Warning!'),_('In Add New KRA point table, Reference to Point No. column cannot be empty'))
                    if wtg == 0.0:
                        raise osv.except_osv(_('Warning!'),_('In Add New KRA point table Weightage can not be 0.0'))
                    search_in_change_sr_no = change_kra_line.search(cr,uid,[('change_points_id','=',x.id),('sr_no','=',sr_no_add)])   
                    if not search_in_change_sr_no:
                        raise osv.except_osv(_('Warning!'),_('Record for reference to point no %s does no exist in the change existing KRA point table.')%(sr_no_add))              
                    if search_in_change_sr_no:
                        for m in change_kra_line.browse(cr,uid,search_in_change_sr_no):
                            typeOfKRA = m.type_of_kra
                            if typeOfKRA != kra_type:
                                raise osv.except_osv(_('Warning!'),_('For reference to point no %s the type does not match with the type of change existing kra point record')%(sr_no_add))  
                


        #Add Reporting Manager and HRO in the followers list    
        subscribe_ids = []
        if x.emp_name and x.emp_name.parent_id and x.emp_name.parent_id.user_id:
            subscribe_ids = [x.emp_name.parent_id.user_id.id,x.emp_name.hro.id]
        subscribe_ids.append( x.emp_name.user_id.id) #related employee added to the follower list
            
        self.message_subscribe_users(cr, SUPERUSER_ID, [x.id], user_ids=subscribe_ids, context=context)
        message = _("Dear Sir, <p> You are requested to approve my New KRA point")
        self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        search_valuel = self.pool.get('kra.points').search(cr,uid,[('points_id','=',x.id)])
        for m in self.pool.get('kra.points').browse(cr,uid,search_valuel):
            self.pool.get('kra.points').write(cr,uid,m.id,{'state':'Submitted to Mgmt'})
        return self.write(cr, uid, ids, {'state': 'Submitted to Mgmt','is_escalated':False}, context=context)
    

    #Function when Reporting Manager Approves the new/change in KRA record and it gets added into the Existing KRA record or a new KRA record gets created
    def approve_request(self, cr, uid, ids, context=None):

        x = self.browse(cr, uid, ids[0])
        form_id = x.id
        emp_name = x.emp_name.id
        designation = x.job.id
        department = x.department.id
        emp_code = x.emp_code
        manager = x.manager_id.id
        join_date = x.join_date
        appraisal_year = x.appraisal_year.id
        escalate = x.is_escalated
        print form_id, emp_name, designation, emp_code, manager, join_date, appraisal_year
        res = self.pool.get('employee.balance.scorecard').search(cr, uid,[('emp_name', '=', emp_name),('appraisal_year','=',appraisal_year)], context=context)
        print res, 'resssss'
        for k in self.pool.get('employee.balance.scorecard').browse(cr,uid,res):
            form = k.id, 
            current_state = k.state
            appYr = k.appraisal_year.id
        if not res:
            create_id1 = self.pool.get('employee.balance.scorecard').create(cr, uid, {'emp_name':emp_name,'emp_code':emp_code,'department':department,'job':designation,'manager_id':manager,'join_date':join_date, 'appraisal_year':appraisal_year}, context=context)
            print create_id1, 'ifffffffff'
        else:
            create_id1 = res[0]
            print create_id1, 'elseeeeeeeeeee'
        
        search_record_change = self.pool.get('kra.points.change').search(cr,uid,[('change_points_id','=',form_id)], context=context)
        search_record_add = self.pool.get('kra.points').search(cr,uid,[('points_id','=',form_id)], context=context)
        search_add_id = self.pool.get('kra.points')
        search_change_id = self.pool.get('kra.points.change')
        print search_record_add
        total_fawr,total_cawr,total_iawr,total_lawr = 0.0,0.0,0.0,0.0
        total_fw,total_fchw,total_cw,total_cchw,total_iw,total_ichw,total_lw,total_lchw = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
        search_in_add = search_add_id.search(cr,uid,[('points_id','=',x.id)])
        for k in search_add_id.browse(cr, uid, search_in_add):
            print 'in the search_in_add'
            approve_refuse = k.yes_no
            if not approve_refuse:
                raise osv.except_osv(_('Warning!'),_('Please select Approved/Refused individually from the Approve column in Add new KRA point table'))
        changed_weightage_f,changed_weightage_c,changed_weightage_i,changed_weightage_l = 0.0,0.0,0.0,0.0
        # if is_escalated == True:
        for c in self.pool.get('kra.points.change').browse(cr, uid, search_record_change):
            formId = c.id
            fkra_id = c.KRA_financial.id
            ckra_id = c.KRA_customer.id
            ikra_id = c.KRA_internal.id
            lkra_id = c.KRA_learning.id
            action = c.action
            typeKra = c.type_of_kra
            cweightage = c.weightage
            cw = c.changed_weightage
            allow = c.yes_no
            sr_no_change = c.sr_no
            # if not allow:
            #     raise osv.except_osv(_('Warning!'),_('Please select yes/no from the approve/refuse column'))    
            if action == "Replace":
                if typeKra == 'Financial':
                    search_in_add = search_add_id.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('yes_no','=','Approved')])
                    print search_in_add, 'Searchhhh in adddd'
                    # self.pool.get('kra.points.copy').create(cr, uid, {'emp_name':emp_name,'app_year':appraisal_year,'sr_no':sr_no_change,'KRA':c.KRA_financial.KRA, 'performance_measure':c.performance_measure,'type_of_kra':'Financial', 'weightage':cweightage,'bsc_id':create_id1,'state':current_state,'action':'Replace','yes_no':'Yes'}, context=context)   
                    for k in search_add_id.browse(cr, uid, search_in_add):
                        kra = k.KRA
                        type_of_kra = k.type_of_kra
                        performance_measure = k.performance_measure
                        aweightage = k.weightage
                        sr_no_add = k.sr_no
                        allow_refuse = k.yes_no  
                        total_fawr += aweightage
                    if total_fawr != c.weightage:
                            raise osv.except_osv(_('Warning!'),_('For type Financial and action Replace, the weightage for new KRA point should be equal to existing KRA point weightage i.e. %s in reference to point no %s')%(c.weightage,sr_no_add))      
                    else:
                        for k in search_add_id.browse(cr, uid, search_in_add):
                            kra = k.KRA
                            type_of_kra = k.type_of_kra
                            performance_measure = k.performance_measure
                            aweightage = k.weightage
                            sr_no_add = k.sr_no
                            allow_refuse = k.yes_no  
                            total_fawr += aweightage    
                            if sr_no_add == sr_no_change:
                                create_id2 = self.pool.get('balance.scorecard.financial').create(cr, uid, {'KRA':kra, 'performance_measure':performance_measure, 'weightage':aweightage,'financial_id':create_id1,'statef':current_state}, context=context)
                        financial_write_id = self.pool.get('balance.scorecard.financial').write(cr, uid, fkra_id, {'active':False}, context=context)
                if typeKra == 'Customer':
                    search_in_add = search_add_id.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('yes_no','=','Approved')])
                    for k in search_add_id.browse(cr, uid, search_in_add):
                        kra = k.KRA
                        type_of_kra = k.type_of_kra
                        performance_measure = k.performance_measure
                        aweightage = k.weightage
                        sr_no_add = k.sr_no
                        total_cawr += aweightage
                    if total_cawr != c.weightage:
                            raise osv.except_osv(_('Warning!'),_('For type Customer and action Replace, the weightage for new KRA point should be equal to existing KRA point weightage i.e. %s in reference to point no %s')%(c.weightage,sr_no_add))      
                    else:    
                        for k in search_add_id.browse(cr, uid, search_in_add):
                            kra = k.KRA
                            type_of_kra = k.type_of_kra
                            performance_measure = k.performance_measure
                            aweightage = k.weightage
                            sr_no_add = k.sr_no
                            allow_refuse = k.yes_no 
                            total_cawr += aweightage
                            if sr_no_add == sr_no_change:
                                create_id3 = self.pool.get('balance.scorecard.customer').create(cr, uid, {'KRA':kra, 'performance_measure':performance_measure, 'weightage':aweightage,'cust_id':create_id1,'statef':current_state}, context=context)
                        customer_write_id = self.pool.get('balance.scorecard.customer').write(cr, uid, ckra_id, {'active':False}, context=context)
                if typeKra == 'Internal Process':
                    search_in_add = search_add_id.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('yes_no','=','Approved')])
                    for k in search_add_id.browse(cr, uid, search_in_add):
                        kra = k.KRA
                        type_of_kra = k.type_of_kra
                        performance_measure = k.performance_measure
                        aweightage = k.weightage
                        sr_no_add = k.sr_no
                        allow_refuse = k.yes_no 
                        total_iawr += aweightage
                    if total_iawr != c.weightage:
                        raise osv.except_osv(_('Warning!'),_('For type Internal Process and action Replace, the weightage for new KRA point should be equal to existing KRA point weightage i.e. %s in reference to point no %s')%(c.weightage,sr_no_add))      
                    else:
                        for k in search_add_id.browse(cr, uid, search_in_add):
                            kra = k.KRA
                            type_of_kra = k.type_of_kra
                            performance_measure = k.performance_measure
                            aweightage = k.weightage
                            sr_no_add = k.sr_no
                            allow_refuse = k.yes_no
                            total_iawr += aweightage
                            if sr_no_add == sr_no_change:
                                create_id4 = self.pool.get('balance.scorecard.internal').create(cr, uid, {'KRA':kra, 'performance_measure':performance_measure, 'weightage':aweightage,'internal_id':create_id1,'statef':current_state}, context=context)
                        internal_write_id = self.pool.get('balance.scorecard.internal').write(cr, uid, ikra_id, {'active':False}, context=context) 
                if typeKra == 'Learning and Growth':
                    search_in_add = search_add_id.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('yes_no','=','Approved')])
                    for k in search_add_id.browse(cr, uid, search_in_add):
                        kra = k.KRA
                        type_of_kra = k.type_of_kra
                        performance_measure = k.performance_measure
                        aweightage = k.weightage
                        sr_no_add = k.sr_no
                        total_lawr += aweightage
                    if total_lawr != c.weightage:
                        raise osv.except_osv(_('Warning!'),_('For type Internal Process and action Replace, the weightage for new KRA point should be equal to existing KRA point weightage i.e. %s in reference to point no %s')%(c.weightage,sr_no_add))      
                    else:                        
                        for k in search_add_id.browse(cr, uid, search_in_add):
                            kra = k.KRA
                            type_of_kra = k.type_of_kra
                            performance_measure = k.performance_measure
                            aweightage = k.weightage
                            sr_no_add = k.sr_no
                            total_lawr += aweightage
                            if sr_no_add == sr_no_change:
                                create_id5 = self.pool.get('balance.scorecard.learning').create(cr, uid, {'KRA':kra, 'performance_measure':performance_measure, 'weightage':aweightage,'learning_id':create_id1,'statef':current_state}, context=context)
                        learning_write_id = self.pool.get('balance.scorecard.learning').write(cr, uid, lkra_id, {'active':False}, context=context)   
            if action == "Change":
                if typeKra == 'Financial':
                    print 'in th iffff'
                    search_in_add = search_add_id.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('yes_no','=','Approved')])
                    changed_weightage_f = c.changed_weightage
                    print changed_weightage_f
                    
                    if search_in_add:
                        for k in search_add_id.browse(cr, uid, search_in_add):
                            kra = k.KRA
                            type_of_kra = k.type_of_kra
                            performance_measure = k.performance_measure
                            aweightage = k.weightage
                            sr_no_add = k.sr_no
                            total_fchw += aweightage
                        if (total_fchw + changed_weightage_f) != c.weightage:
                            raise osv.except_osv(_('Warning!'),_('For type Financial and action change, the weightage for new KRA point and the changed weightage for existing KRA should be %s in total in reference to point no %s')%(c.weightage,sr_no_add))   
                        else:
                            if changed_weightage_f:
                                self.pool.get('balance.scorecard.financial').write(cr, uid, fkra_id, {'weightage':changed_weightage_f}) 
                            for k in search_add_id.browse(cr, uid, search_in_add):
                                kra = k.KRA
                                type_of_kra = k.type_of_kra
                                performance_measure = k.performance_measure
                                aweightage = k.weightage
                                sr_no_add = k.sr_no
                                total_fchw += aweightage
                                self.pool.get('balance.scorecard.financial').create(cr, uid, {'KRA':kra, 'performance_measure':performance_measure, 'weightage':aweightage,'financial_id':create_id1,'statef':current_state}, context=context)   
                    else:
                        print 'in the else'
                        for c in self.pool.get('kra.points.change').browse(cr, uid, search_record_change):                        
                            self.pool.get('balance.scorecard.financial').write(cr, uid, fkra_id, {'weightage':changed_weightage_f})     
                if typeKra == 'Customer':
                    print 'in th iffff'
                    search_in_add = search_add_id.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('yes_no','=','Approved')])
                    changed_weightage_c = c.changed_weightage
                    
                    if search_in_add:
                        for k in search_add_id.browse(cr, uid, search_in_add):
                            kra = k.KRA
                            type_of_kra = k.type_of_kra
                            performance_measure = k.performance_measure
                            aweightage = k.weightage
                            sr_no_add = k.sr_no
                            total_cchw += aweightage
                        if c.weightage != (changed_weightage_c + total_cchw):
                            raise osv.except_osv(_('Warning!'),_('For type Customer and action change, the weightage for new KRA point and the changed weightage for existing KRA should be %s in total in reference to point no %s')%(c.weightage,sr_no_add))
                        else:
                            if changed_weightage_c:
                                self.pool.get('balance.scorecard.customer').write(cr, uid, ckra_id, {'weightage':changed_weightage_c})
                            for k in search_add_id.browse(cr, uid, search_in_add):
                                kra = k.KRA
                                type_of_kra = k.type_of_kra
                                performance_measure = k.performance_measure
                                aweightage = k.weightage
                                sr_no_add = k.sr_no
                                total_cchw += aweightage   
                                self.pool.get('balance.scorecard.customer').create(cr, uid, {'KRA':kra, 'performance_measure':performance_measure, 'weightage':aweightage,'cust_id':create_id1,'statef':current_state}, context=context)
                    else:
                        print 'in the else'
                        for c in self.pool.get('kra.points.change').browse(cr, uid, search_record_change):                        
                            self.pool.get('balance.scorecard.customer').write(cr, uid, ckra_id, {'weightage':changed_weightage_c})
                        
                if typeKra == 'Internal Process' :
                    search_in_add = search_add_id.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('yes_no','=','Approved')])
                    changed_weightage_i = c.changed_weightage
                    if search_in_add:
                        for k in search_add_id.browse(cr, uid, search_in_add):
                            kra = k.KRA
                            type_of_kra = k.type_of_kra
                            performance_measure = k.performance_measure
                            aweightage = k.weightage
                            sr_no_add = k.sr_no
                            total_ichw += aweightage
                        if c.weightage != (changed_weightage_i + total_ichw):
                            raise osv.except_osv(_('Warning!'),_('For type Internal Process and action change, the weightage for new KRA point and the changed weightage for existing KRA should be %s in total in reference to point no %s')%(c.weightage,sr_no_add)) 
                        else:
                            if changed_weightage_i:
                                self.pool.get('balance.scorecard.internal').write(cr, uid, ikra_id, {'weightage':changed_weightage_i}) 
                            for k in search_add_id.browse(cr, uid, search_in_add):
                                kra = k.KRA
                                type_of_kra = k.type_of_kra
                                performance_measure = k.performance_measure
                                aweightage = k.weightage
                                sr_no_add = k.sr_no
                                total_ichw += aweightage
                                create_id4 = self.pool.get('balance.scorecard.internal').create(cr, uid, {'KRA':kra, 'performance_measure':performance_measure, 'weightage':aweightage,'internal_id':create_id1,'statef':current_state}, context=context)
                    else:
                        for c in self.pool.get('kra.points.change').browse(cr, uid, search_record_change):                        
                            self.pool.get('balance.scorecard.internal').write(cr, uid, ikra_id, {'weightage':changed_weightage_i}) 
                if typeKra == 'Learning and Growth':
                    search_in_add = search_add_id.search(cr,uid,[('points_id','=',x.id),('sr_no','=',sr_no_change),('yes_no','=','Approved')])
                    changed_weightage_l = c.changed_weightage
                    
                    if search_in_add:
                        for k in search_add_id.browse(cr, uid, search_in_add):
                            kra = k.KRA
                            type_of_kra = k.type_of_kra
                            performance_measure = k.performance_measure
                            aweightage = k.weightage
                            sr_no_add = k.sr_no
                            total_lchw += aweightage
                        if c.weightage != (changed_weightage_l + total_lchw):
                            raise osv.except_osv(_('Warning!'),_('For type Learning and Growth, for action change, the weightage for new KRA point and the changed weightage for existing KRA should be %s in total in reference to point no %s')%(c.weightage,sr_no_add)) 
                        else:
                            if changed_weightage_l:
                                self.pool.get('balance.scorecard.learning').write(cr, uid, lkra_id, {'weightage':changed_weightage_l}) 
                            for k in search_add_id.browse(cr, uid, search_in_add):
                                kra = k.KRA
                                type_of_kra = k.type_of_kra
                                performance_measure = k.performance_measure
                                aweightage = k.weightage
                                sr_no_add = k.sr_no
                                total_lchw += aweightage
                                create_id5 = self.pool.get('balance.scorecard.learning').create(cr, uid, {'KRA':kra, 'performance_measure':performance_measure, 'weightage':aweightage,'learning_id':create_id1,'statef':current_state}, context=context)
                    else:
                        for c in self.pool.get('kra.points.change').browse(cr, uid, search_record_change):
                            self.pool.get('balance.scorecard.learning').write(cr, uid, lkra_id, {'weightage':changed_weightage_l}) 
    
        message = _("Request for adding a New KRA point is approved.")
        self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        search_valuel = self.pool.get('kra.points').search(cr,uid,[('points_id','=',x.id)])
        for m in self.pool.get('kra.points').browse(cr,uid,search_valuel):
            self.pool.get('kra.points').write(cr,uid,m.id,{'state':'Approved'})
        return self.write(cr, uid, ids, {'state': 'Approved','flag':True}, context=context)

    
    def refuse_all(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        search_valuel = self.pool.get('kra.points').search(cr,uid,[('points_id','=',x.id)])
        for m in self.pool.get('kra.points').browse(cr,uid,search_valuel):
            self.pool.get('kra.points').write(cr,uid,m.id,{'state':'Refused'})
        message = _("All points are refused")
        self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        return self.write(cr, uid, ids, {'state': 'Refused','is_escalated':True,'flag':False}, context=context)

    def escalate(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        search_valuel = self.pool.get('kra.points').search(cr,uid,[('points_id','=',x.id)])
        for m in self.pool.get('kra.points').browse(cr,uid,search_valuel):
            self.pool.get('kra.points').write(cr,uid,m.id,{'state':'Escalated'})
        message = _("Some points are approved and some are refused, please change the weightage for approved points and resubmit it.")
        self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        return self.write(cr, uid, ids, {'state': 'Escalated','is_escalated':True,'flag':False}, context=context)


    #function when new KRA request is refused
    def refuse_request(self, cr, uid, ids, context=None):
        return {
                'type': 'ir.actions.act_window',
                'name': _('KRA refuse Wizard'),
                'res_model': 'kra.refuse.wizard',
                'res_id': ids[0],
                'view_type': 'form',
                'view_mode': 'form',
               # 'view_id': form_view_id,
                'target': 'new',
                'nodestroy': True,
                }
        
    
    #function when a KRA request record is set to Draft
    def set_draft(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        search_valuel = self.pool.get('kra.points').search(cr,uid,[('points_id','=',x.id)])
        for m in self.pool.get('kra.points').browse(cr,uid,search_valuel):
            self.pool.get('kra.points').write(cr,uid,m.id,{'state':'New'})
        self.write(cr, uid, ids, { 'state': 'New','flag':False}, context=context)
        return True
    
class kra_points_change(osv.osv):
    _name = "kra.points.change"
    _description = "Change Existing KRA Points"
    
    _columns = {
        'change_points_id': fields.many2one('request.new.kra', 'Change Existing KRA'),
        'sr_no': fields.integer('Sr.No.', required=True),
        'empid': fields.many2one('hr.employee', 'Employee'), 
#         'KRA_financial':fields.many2one('balance.scorecard.financial','KRA (As identified for corresponding period)', domain="_get_points"),
        'KRA_financial':fields.many2one('balance.scorecard.financial', 'KRA-Financial',domain="[('financial_id.emp_name','=',parent.emp_name),('financial_id.appraisal_year','=',parent.appraisal_year),('type','=','Financial'),('active','=',True)]"),
        'KRA_customer':fields.many2one('balance.scorecard.customer','KRA-Customer',domain="[('cust_id.emp_name','=',parent.emp_name),('cust_id.appraisal_year','=',parent.appraisal_year),('type','=','Customer'),('active','=',True)]"),
        'KRA_internal':fields.many2one('balance.scorecard.internal','KRA-Internal Process',domain="[('internal_id.emp_name','=',parent.emp_name),('internal_id.appraisal_year','=',parent.appraisal_year),('type','=','Internal Process'),('active','=',True)]"),
        'KRA_learning':fields.many2one('balance.scorecard.learning','KRA-Learning & Growth',domain="[('learning_id.emp_name','=',parent.emp_name),('learning_id.appraisal_year','=',parent.appraisal_year),('type','=','Learning and Growth'),('active','=',True)]"),
        'type_of_kra':fields.selection([('Financial','Financial'),('Customer','Customer'),('Internal Process','Internal Process'),('Learning and Growth','Learning and Growth')], 'Type',required=True),
        'performance_measure':fields.char('Performance Measure',required=True),
        'weightage':fields.float('Weightage (W) 100%',required=True),
        'action':fields.selection([('Change','Change'),('Replace','Replace')],'Action',required=True),
        'changed_weightage':fields.float('Changed Weightage (W) 100%'),
        'yes_no': fields.selection([('Yes','Yes'),('No','No')], 'Approve/Refuse'),
        'state': fields.selection([('New', 'New'),('Submitted to Mgmt', 'Submitted to Manager'),('Approved', 'Approved By Manager'),('Refused', 'Refused')], 'Status'),    
        
    }
    

    _defaults = {
        'state': 'New',
        'sr_no': 0,
    }

    
    def unlink(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids, context=context):
            search_hro = self.pool.get('res.users').search(cr, uid, [('is_hro', '=', True)])
            print rec.state
            if rec.state != 'New':
                raise osv.except_osv(_('Warning!'),_('You can only delete Draft records'))
        return super(kra_points_change, self).unlink(cr, uid, ids, context)

    def onchange_kra_financial(self, cr, uid, ids, KRA_financial, context=None):
        value = {'performance_measure': False,'weightage': False}
        if KRA_financial:
            fin = self.pool.get('balance.scorecard.financial').browse(cr, uid, KRA_financial)
            value['performance_measure'] = fin.performance_measure
            value['weightage'] = fin.weightage
            print value
        return {'value': value}            

             
    def onchange_kra_customer(self, cr, uid, ids, KRA_customer, context=None):
        value = {'performance_measure': False,'weightage': False}
        if KRA_customer:
            cus = self.pool.get('balance.scorecard.customer').browse(cr, uid, KRA_customer)
            value['performance_measure'] = cus.performance_measure
            value['weightage'] = cus.weightage
            
        return {'value': value}
    
    def onchange_kra_internal(self, cr, uid, ids, KRA_internal, context=None):
        value = {'performance_measure': False,'weightage': False}
        if KRA_internal:
            inte = self.pool.get('balance.scorecard.internal').browse(cr, uid, KRA_internal)
            value['performance_measure'] = inte.performance_measure
            value['weightage'] = inte.weightage
            
        return {'value': value}
    
    def onchange_kra_learning(self, cr, uid, ids, KRA_learning, context=None):
        value = {'performance_measure': False,'weightage': False}
        if KRA_learning:
            lea = self.pool.get('balance.scorecard.learning').browse(cr, uid, KRA_learning)
            value['performance_measure'] = lea.performance_measure
            value['weightage'] = lea.weightage
            
        return {'value': value}
    
    
    
class kra_points(osv.osv):
    _name = "kra.points"
    _description = "Employee KRA Points"
        

    _columns = {
        'points_id': fields.many2one('request.new.kra', 'Add New KRA'),
        'sr_no': fields.integer('Reference To Point No.', required=True),
        'KRA':fields.char('KRA (As identified for corresponding period)',required=True),
        'type_of_kra':fields.selection([('Financial','Financial'),('Customer','Customer'),('Internal Process','Internal Process'),('Learning and Growth','Learning and Growth')], 'Type',required=True),
        'performance_measure':fields.char('Performance Measure',required=True),
        'weightage':fields.float('Weightage (W) 100%',required=True),   
        'yes_no': fields.selection([('Approved','Approved'),('Refused','Refused')], 'Approve'),   
        'state': fields.selection([('New', 'New'),('Submitted to Mgmt', 'Submitted to Manager'),('Escalated','Escalated'),('Approved', 'Approved By Manager'),('To be Refused', 'To be Refused'),('Refused', 'Refused')], 'Status'),    
        'character': fields.char('Character')
    }

    _defaults = {
        'state': 'New',
        'sr_no': 0,
    }

    def onchange_type_of_kra(self, cr, uid, ids, type_of_kra, context=None):
        value = {'performance_measure': False,'weightage': False}
        if KRA_learning:
            lea = self.pool.get('balance.scorecard.learning').browse(cr, uid, KRA_learning)
            value['performance_measure'] = lea.performance_measure
            value['weightage'] = lea.weightage
            
        return {'value': value}

    # def onchange_approved(self, cr, uid, ids, yes_no, points_id, context=None):
    #     print points_id,yes_no,ids, 'points_idsssssssss'         
    #     parent_class = self.pool.get('request.new.kra')
    #     p = False
    #     value = False
    #     no_of_rec = self.search(cr,uid,[('points_id','=', points_id)])
    #     print no_of_rec, 'no of records'
    #     ind = no_of_rec.index(ids[0])
    #     self.write(cr,uid,ids,{'character':yes_no})
    #     c = self.browse(cr,uid,no_of_rec)
    #     l_char =[]
    #     for j in c:
    #         val_char = str(j.character)
    #         l_char.append(val_char)
    #     print l_char, 'char list'
    #     print no_of_rec, 'no of records'
    #     print len(no_of_rec), 'length'
    #     search_approved_rec =  self.search(cr,uid,[('points_id','=',points_id),('character','=','Approved')])
    #     print search_approved_rec, len(search_approved_rec), 'length of app rec'
    #     if 'Refused' in l_char:
    #         approved_var = True
    #         print approved_var, 'valls'
    #         value = parent_class._check_approval(cr,uid,ids,approved_var,field_names=None, arg=None, context=None)
    #         print 'Escalate --> Partial Approval',value
    #     else:
    #         approved_var = False
    #         value = parent_class._check_approval(cr,uid,ids,approved_var,field_names=None, arg=None, context=None)
    #     return value
        



        
class kra_interview(osv.osv):
    _name = 'kra.interview'
    _inherit =  'mail.thread'
    _description = 'Appraisal Interview'


    def _app_yr_get(self, cr, uid, context=None):
        today = datetime.today().date()
        yrs = self.pool.get('account.fiscalyear')
        if str(today)>='2016-02-01' and str(today)<='2016-12-31':
            search_add_id = yrs.search(cr,uid,[('name','=','2015-2016')])
        elif str(today)>='2017-02-01' and str(today)<='2017-12-31':
            search_add_id = yrs.search(cr,uid,[('name','=','2016-2017')])  
        else:
            search_add_id = ''
        return search_add_id[0]

    def check_existance(self, cr, uid, ids, context=None):
        if context is None:
                context = {}
        self_obj = self.browse(cr, uid, ids[0], context=context)
        field1 = self_obj.user_to_review_id.id
        field2 = self_obj.appraisal_year.id
        search_ids = self.search(cr, uid, [('user_to_review_id', '=', field1),('appraisal_year', '=' , field2)], context=context)
        res = True
        if len(search_ids) > 1:
            raise osv.except_osv(_('Warning!'),_('Appraisal Meeting record for %s for the financial year %s has been already processed')%(self_obj.user_to_review_id.name,self_obj.appraisal_year.name))
            res = False
        return res

    _columns = {
        'company_id': fields.many2one('res.company', 'Company'),
        'name': fields.char('Description'),
        'date_review': fields.date('Date', select=True),
        'appraisal_year': fields.many2one('account.fiscalyear', 'Appraisal Year'),
        'user_to_review_id': fields.many2one('hr.employee', 'Employee', required=True),
        'manager_id': fields.many2one('hr.employee', 'Interviewer', domain="[('manager', '=', True)]"),
#         'date_deadline': fields.date('Deadline Date'),
        'date_interview': fields.datetime('Interview Date', required=True),
        'note': fields.text('Note'),
        'date_time_field':fields.char('Date Time field'),
        'state': fields.selection([('draft', 'Draft'),('submitted to reporting manager','Submitted to Reporting Manager'),('cancel','Cancelled'),('waiting_answer','Approved By Reporting Manager'),('done','Accepted By Employee')],'Status')
    }
    
    _defaults = {
            'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'kra.interview', context=c),
            'name': 'Appraisal Meeting Request',
            'state': 'draft',
            'appraisal_year': _app_yr_get,
            'date_review': fields.date.context_today,
                 }


    _constraints = [(check_existance,'KRA for the employee for the given financial year has been already processed', ['user_to_review_id','appraisal_year'])]

    def onchange_employee(self, cr, uid, ids, user_to_review_id, context=None):
        value = {'manager_id': False }
        if user_to_review_id:
            emp = self.pool.get('hr.employee').browse(cr, uid, user_to_review_id)
            value['manager_id'] = emp.parent_id.id
        return {'value': value}
    
    #Function for Appraisal Meeting request to Reporting Manager of an Employee
    def survey_req_waiting_answer(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        emp = x.user_to_review_id.name
        manager = x.manager_id.name
        emp_id = x.user_to_review_id.id
        appYr = x.appraisal_year.id
        print appYr, 'appraisal_year'
        today = datetime.today().date()
        bscID = self.pool.get('employee.balance.scorecard').search(cr, uid,[('emp_name', '=', emp_id),('appraisal_year','=',appYr)], context=context)
        if bscID:
            for m in self.pool.get('employee.balance.scorecard').browse(cr,uid,bscID):
                state = m.state
                if state == 'Submitted To Manager':
                    subscribe_ids = []
                    if x.user_to_review_id and x.user_to_review_id.parent_id and x.user_to_review_id.parent_id.user_id:
                        subscribe_ids = [x.user_to_review_id.parent_id.user_id.id,x.user_to_review_id.hro.id,52]
                        self.message_subscribe_users(cr, SUPERUSER_ID, [x.id], user_ids=subscribe_ids, context=context)
                        message = _("Hi %s, <p> You are requested to approve the Appraisal Meeting request for %s.") % (manager, emp)
                        self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        #               subscribe_ids.append( x.emp_name.user_id.id) #related employee added to the follower list
                        self.write(cr, uid, ids, { 'state': 'submitted to reporting manager'}, context=context)
                else:
                    raise osv.except_osv(('Warning!!'),('You can only create Review Request record when Appraisal form is in Submitted To Manager state.'))
        elif not bscID:
            raise osv.except_osv(('Warning!!'),('You cannot create review request record if there is no record for Appraisal.'))
        
        

    #Function when Reporting Manager accepts the request and send the request to Employee
    def survey_req_done(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        emp = x.user_to_review_id.name
        interview_date = x.date_interview
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Asia/Kolkata')

        utc = datetime.strptime(interview_date, '%Y-%m-%d %H:%M:%S')
        utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        central = utc.astimezone(to_zone)
        central = str(central)
        central_split = central.split('+')
        central_split1 = central_split[0].split(' ') 
        central_date = central_split1[0]
        central_time = central_split1[1]
        central_date = datetime.strptime(central_date ,"%Y-%m-%d").strftime("%d/%m/%Y")
        date_time_field = str(central_date) + " " + str(central_time)
        if x.user_to_review_id:
            subscribe_ids = [x.user_to_review_id.user_id.id]
#         subscribe_ids.append( x.emp_name.user_id.id) #related employee added to the follower list
            
        self.message_subscribe_users(cr, SUPERUSER_ID, [x.id], user_ids=subscribe_ids, context=context)
        message = _("Hi %s,<p>Your appraisal meeting with your reporting manager has been scheduled on date: %s and time: %s. <p>Kindly make yourself available for the Meeting. <p><center><b>BEST OF LUCK!!!!") % (emp,central_date,central_time)
        self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        self.write(cr, uid, ids, { 'state': 'waiting_answer','date_time_field':date_time_field}, context=context)
    
    #Function when Employee Accepts the review request
    def survey_req_accepted(self, cr, uid, ids, context=None):
        x = self.browse(cr, uid, ids[0])
        emp = x.user_to_review_id.name
        emp_id = x.user_to_review_id.id
        appYr = x.appraisal_year.id
        name = 'Appraisal Process for '+ str(emp)
        if x.user_to_review_id.user_id.id != uid:
            raise osv.except_osv(_('Warning!'),_('You cannot accept Appraisal Meeting request for the Appraisee.'))
        print appYr, 'appraisal_year'
        today = datetime.today().date()
        date_after_7Days = today + timedelta(days=7)
        bscID = self.pool.get('employee.balance.scorecard').search(cr, uid,[('emp_name', '=', emp_id),('appraisal_year','=',appYr)], context=context)
        if bscID:
            search_valuef = self.pool.get('balance.scorecard.financial').search(cr,uid,[('financial_id','=',bscID[0])])
            search_valuec = self.pool.get('balance.scorecard.customer').search(cr,uid,[('cust_id','=',bscID[0])])
            search_valuei = self.pool.get('balance.scorecard.internal').search(cr,uid,[('internal_id','=',bscID[0])])
            search_valuel = self.pool.get('balance.scorecard.learning').search(cr,uid,[('learning_id','=',bscID[0])])
            for m in self.pool.get('balance.scorecard.financial').browse(cr,uid,search_valuef):
                self.pool.get('balance.scorecard.financial').write(cr,uid,m.id,{'statef':'Appraisal Meeting'})
            for m in self.pool.get('balance.scorecard.customer').browse(cr,uid,search_valuec):
                self.pool.get('balance.scorecard.customer').write(cr,uid,m.id,{'statef':'Appraisal Meeting'})
            for m in self.pool.get('balance.scorecard.internal').browse(cr,uid,search_valuei):
                self.pool.get('balance.scorecard.internal').write(cr,uid,m.id,{'statef':'Appraisal Meeting'})
            for m in self.pool.get('balance.scorecard.learning').browse(cr,uid,search_valuel):
                self.pool.get('balance.scorecard.learning').write(cr,uid,m.id,{'statef':'Appraisal Meeting'})
        self.pool.get('employee.balance.scorecard').write(cr,uid,bscID[0],{'state':'Appraisal Meeting','meeting_ok':True,'date_kra':today,'date_after_7Days':date_after_7Days})     
        message = _("Hi, <p>%s has accepted the request for Appraisal meeting.")%(emp)
        self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        self.write(cr, uid, ids, { 'state': 'done','date_review':today}, context=context)

    #Function when Review record is set to Draft
    def survey_req_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, { 'state': 'draft'}, context=context)
        return True

    #Function when review Record is refused
    def survey_req_cancel(self, cr, uid, ids, context=None):
        message = _("Request Refused")
        self.message_post(cr, uid, ids, body = message, type='comment', subtype='mt_comment', context = context)
        self.write(cr, uid, ids, { 'state': 'cancel'}, context=context)
        return True
    
    

    def reminder_review_interview(self,cr,uid,context=None):
        rec_search = self.search(cr, uid, [('id', '>', 0)], context=None)
        print rec_search
        for x in self.browse(cr,uid,rec_search):
            count = 0
            current_id = x.id
            interview_date = x.date_interview
            current_state = x.state
            print interview_date
            emp = x.user_to_review_id.name
            manager = x.manager_id.name
            emp_id = x.user_to_review_id.id
            appYr = x.appraisal_year.id
            print appYr, 'appraisal_year'
            today = datetime.today().date()
            bscID = self.pool.get('employee.balance.scorecard').search(cr, uid,[('emp_name', '=', emp_id),('appraisal_year','=',appYr)], context=context)
            if bscID:
                for m in self.pool.get('employee.balance.scorecard').browse(cr,uid,bscID):
                    state = m.state
                    if state == 'Appraisal Meeting':
                        if interview_date:
                            new_interview_date = datetime.strptime(str(interview_date[0:10]), "%Y-%m-%d").date()
                            today = datetime.now()
                            today = datetime.today().date()
                            tenure = relativedelta(new_interview_date,today)
                            print tenure.days, 'tenuree days'
                            print tenure
                            today_day = today.day
                            today_month = today.month
                            print today_day, today_month                
                            if current_state == "done" and tenure.days in (2,4,6):
                                search_template_record = self.pool.get('email.template').search(cr,uid,[('model_id.model','=','kra.interview'),('lang','=','Interview Reminder')], context=context)
                                if search_template_record:
                                    print "ggggggggggggggggggggggggggggggggggggggggggggggg", search_template_record
                                    print 'I am intoooo review interview reminder definition'
                                    self.pool.get('email.template').send_mail(cr, uid, search_template_record[0], current_id, force_send=True, context=context)
                                    print "Send Reminder"
                                    count = count+1
                                return True
                            if current_state == "done" and tenure.days == 7:
                                search_template_record = self.pool.get('email.template').search(cr,uid,[('model_id.model','=','kra.interview'),('lang','=','Interview Reminder')], context=context)
                                if search_template_record:
                                    print "ggggggggggggggggggggggggggggggggggggggggggggggg", search_template_record
                                    print 'I am intoooo review interview reminder definition'
                                    self.pool.get('email.template').send_mail(cr, uid, search_template_record[0], current_id, force_send=True, context=context)
                                    print "Send Reminder"
                                    count = count+1
                                return True
   

kra_interview()

class export_table_config(osv.osv):
    _name = 'export.table.config'
    _columns = {
                'path':fields.char('Export File Storage Path')
    }

    def create(self, cr, uid, vals, context=None):
        path = vals.get('path')
        if not os.path.exists(path):
            raise osv.except_osv(('Warning!!'),('Directory does not exist.'))
        self_ids = self.search(cr, uid, [])
        if len(self_ids) >= 1:
            raise osv.except_osv(('Warning!!'),('One active File Store Path is already there. Please edit in that record.'))
        res = super(export_table_config,self).create(cr, uid, vals, context=context)
        return res

    def write(self, cr, uid, ids, vals, context=None):
        path = vals.get('path')
        if path and not os.path.exists(path):
            raise osv.except_osv(('Warning!!'),('Directory does not exist.'))
        res = super(export_table_config,self).write(cr, uid, ids, vals, context=context)
        return res

export_table_config()


class kra_report(osv.osv):
    _name = 'kra.report'
    _description = 'Analysis Report'
    _auto = False
    _columns = {
        
        'count':fields.integer('Value', readonly=True),
        'total_score': fields.float('Total Score',readonly=True),
        'sections': fields.selection([('Financial','Financial'),('Customer','Customer'),('Learning and Growth','Learning and Growth'),('Internal Process','Internal Process')], 'Sections',readonly=True) ,                 
        'appraisalyr': fields.char('Appraisal Year',readonly=True)
    }
    
      
class kra_fetch_dashboard(osv.osv):
    _name='kra.fetch.dashboard'
    _description='KRA Fetch dashboard'

    def _employee_get(self, cr, uid, ids,context=None):   
        result = {}
        if uid != 43:     
            print 'in the graphs '
            ids_p = self.pool.get('hr.employee').search(cr, uid, [('parent_id.user_id','=',uid)], context=context)
            emp_list = []
            for empl in self.pool.get('hr.employee').browse(cr, uid, ids_p):
                emp_id = empl.id
                emp_list.append('')
                emp_list.append(emp_id)
                print emp_list
                print empl.name
            return emp_list
        else:
            ids_p = self.pool.get('hr.employee').search(cr, uid, [('id','>',0),('active','=',True)], context=context)
            emp_list = []
            for empl in self.pool.get('hr.employee').browse(cr, uid, ids_p):
                emp_id = empl.id
                emp_list.append('')
                emp_list.append(emp_id)
                print emp_list
                print empl.name
            return emp_list

    _columns={ 
        'name': fields.char('Name'),          
        # 'employee_id': fields.many2one('hr.employee', 'Employee Name', required=True, domain="['|',('hro','=',uid),'|',('parent_id.parent_id.user_id','=',uid),('parent_id.user_id','=',uid)]"),
        'employee_id': fields.many2one('hr.employee', 'Employee Name', required=True),
        'appraisal_year': fields.many2one('account.fiscalyear', 'Appraisal Year'),
        'bsc_id':fields.many2one('employee.balance.scorecard', 'BSC')
    }    
    _defaults={
        'name': 'KRA Graph Analysis',
        'employee_id': _employee_get,
    }
    
    #Function for Sectionwise Graph
    def fetch_graph(self,cr,uid,ids,employee_id,context=None):
        cr.execute("drop view if exists kra_report")
        current_emp = self.browse(cr, uid, ids[0])
        print current_emp.employee_id.name, 'employee name'
        empName = current_emp.employee_id.id
        app = current_emp.appraisal_year.id
        empl_name = current_emp.employee_id.name
        app_year = current_emp.appraisal_year.name
        print app , 'pppppppppp'
        bscID = self.pool.get('employee.balance.scorecard').search(cr, uid,[('emp_name', '=', empName),('appraisal_year','=',app)], context=context)
        # drop_view_if_exists(cr,'kra_report')
        bsc =''
        if not bscID:
            raise osv.except_osv(('Warning!!'),('No Appraisal record for %s for year %s')%(empl_name,app_year))
        if bscID:
            bsc = bscID[0]
            print bsc
        cr.execute("select id from ir_ui_view where model='kra.report' and type='graph' and name='kra.reports.graph'")
        view_id = map(lambda x: x[0], cr.fetchall())
        if view_id:
            view_id = view_id[0]
        else:
            view_id = False
        if context is None:
            context={}
        print view_id, 'view ID'  
        if bsc and view_id:
            cr.execute("""CREATE or REPLACE VIEW kra_report AS
                    (   
                        SELECT ROW_NUMBER() OVER () as id,
                               p.total_score as total_score,
                               p.count as count,
                               p.sections as sections
                        FROM (
                                    select
                                    sum(weighted_scoref) as total_score,
                                    sum(count(*)) OVER (order by type) as count,
                                    type as sections
                                    from balance_scorecard_financial
                                    where type = 'Financial' and active='t'
                                    and financial_id = %s
                                    group by type

                                    UNION

                                    select
                                    sum(weighted_scorec) as total_score,
                                    sum(count(*)) OVER (order by type) as count,
                                    type as sections
                                    from balance_scorecard_customer
                                    where type = 'Customer' and active='t'
                                    and cust_id = %s
                                    group by type

                                    UNION

                                    select
                                    sum(weighted_scorei) as total_score,
                                    sum(count(*)) OVER (order by type) as count,
                                    type as sections
                                    from balance_scorecard_internal
                                    where type = 'Internal Process' and active='t'
                                    and internal_id = %s
                                    group by type

                                    UNION

                                    select
                                    sum(weighted_scorel) as total_score,
                                    sum(count(*)) OVER (order by type) as count,
                                    type as sections
                                    from balance_scorecard_learning
                                    where type = 'Learning and Growth' and active='t'
                                    and learning_id = %s
                                    group by type


                     )AS p 
                    )
                    """%(bsc,bsc,bsc,bsc))
            
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'graph',
                'view_mode': 'graph',
                'res_model': 'kra.report',
                'view_id': view_id,
                'target': 'new',
                'context': {},
            }
        else:
            return False

    #Function for Yearwise Graph
    def fetch_graph_yearwise(self,cr,uid,ids,employee_id,context=None):
        cr.execute("drop view if exists kra_report")
        current_emp = self.browse(cr, uid, ids[0])
        print current_emp
        print current_emp.employee_id.name, 'employee name'
        empName = current_emp.employee_id.id 
        empl_name = current_emp.employee_id.name       
        print empName,'emp name'
        bscID = self.pool.get('employee.balance.scorecard').search(cr, uid,[('emp_name', '=', empName)], context=context)
        print bscID, 'BalanceSC list'
        bsc =''
        if not bscID:
            raise osv.except_osv(('Warning!!'),('No Appraisal record for %s')%(empl_name,))
        if bscID:
            bsc = bscID[0]
            print bsc
        idList = []
        ayList = []
        for m in self.pool.get('employee.balance.scorecard').browse(cr,uid,bscID):
            main_id = m.id
            app_id = m.appraisal_year.id
            idList.append(main_id)
            ayList.append(app_id)
        print idList, ayList, 'List of values;'
        

        cr.execute("select id from ir_ui_view where model='kra.report' and type='graph' and name='kra.reports.year.graph'")
        view_id = map(lambda x: x[0], cr.fetchall())
        if view_id:
            view_id = view_id[0]
        else:
            view_id = False
        if context is None:
            context={}
        print view_id, 'view ID'  
        if bscID and view_id:            
            
            cr.execute("""CREATE or REPLACE VIEW kra_report AS
                    (   
                        SELECT ROW_NUMBER() OVER () as id,
                               p.total_score as total_score,
                               p.appraisalyr as appraisalyr
                        FROM (
                               select employee_balance_scorecard.total_score,
                               account_fiscalyear.name as appraisalyr 
                               from employee_balance_scorecard join account_fiscalyear 
                               on account_fiscalyear.id=employee_balance_scorecard.appraisal_year 
                               where emp_name = %s                              
                               group by employee_balance_scorecard.total_score,account_fiscalyear.name
                     )AS p 
                    )
                    """%(empName))
        
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'graph',
                'view_mode': 'graph',
                'res_model': 'kra.report',
                'view_id': view_id,
                'target': 'new',
                'context': {},
            }
        else:
            return False

class reason_refusal(osv.osv):
    _name = "reason.refusal"
    _description = "Reason for Refusal"
    

    _columns = {

        'name':fields.char('Description'),
        'refusal_reason':fields.text('Reason for Refusal'),
        
        }

reason_refusal()
