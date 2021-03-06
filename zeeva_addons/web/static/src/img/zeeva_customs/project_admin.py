# -*- coding: utf-8 -*-

import math
import Image
import base64

from osv import fields,osv
import tools
import pooler
from tools.translate import _

import time

class project_project(osv.osv):
    _inherit = 'project.project'
    
    #def _get_issue_qty(self, cr, uid, ids, name, arg, context=None):
        #res = {}
        #issue_pool = self.pool.get('project.issue')
        
        #for project in self.browse(cr, uid, ids, context=context):
            #issue_pool.search(cr, uid, ('', '=', project), context=None)

            #res[project.id] = project.employee_ids[0].job_id.name
        #return res
    
    _columns = {
        #info
        'creation_user': fields.many2one('res.users','Created by'),
        'creation_date': fields.date('Created on'),

        #'name': fields.char('Project code', size=64, required=False),
        #'issue_qty': fields.function(_get_issue_qty, string='Issues No', type='integer'), #TODO optimization store etc
        
        #project details
        'category': fields.selection([('new','New order'),('reorder','Re-order')], 'Category'),
        'supplier_id': fields.many2one('res.partner', 'Supplier'),
        
        #products
        'raw_product_id': fields.many2one('product.template', 'Raw product'),
        'finished_product_id': fields.many2one('product.product', 'Finished product'),
        
        #artwork
        'artwork_received': fields.boolean('Artwork received'),
        'packaging_type': fields.char('Packaging type', size=128),
        'packaging_finishing': fields.char('Packaging finishing', size=128),
        'material_used': fields.char('Material used', size=128),
        'card_thickness': fields.char('Card thickness', size=128),
        'blister_thickness': fields.char('Blister thickness', size=128),
        'design_status': fields.selection([('draft','To do'),('open','In Progress'),('done','Done')], 'Design status'),
        'remarks': fields.text('Remarks'),

    }
    
    #_order = 'name asc'
    
    _defaults = {
        'name': '/',
        'use_tasks': True,
        'design_status': 'draft',
        'state': 'draft',
        #'privacy_visibility': 'followers',
        
    }
    
    def create(self, cr, uid, vals, context=None):
        
        if ('name' not in vals) or (vals.get('name')=='/'):
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'project.admin')
            
        vals['creation_user'] = uid
        vals['creation_date'] = fields.date.context_today(self,cr,uid,context=context)
        
        #print vals

        return super(project_project,self).create(cr, uid, vals, context)
    
    #def onchange_finished_product(self, cr, uid, ids, product_id, context=None):
        #result = {}
        #customer = 0
        
        #if product_id:
            #product_obj = self.pool.get('product.product').browse(cr, uid, product_id, context=None)
            #customer = product_obj.zeeva_partner_id
            
        #result = {'value': {'customer_id': customer.id}}
        
        #return result
    
    def _change_status(self, cr, uid, ids, next, *args):
        """
            go to the next status
            if next is False, go to previous status
        """
        for task in self.browse(cr, uid, ids):
            if next == True:
                if task.design_status == 'draft':
                    self.write(cr, uid, task.id, {'design_status': 'open'})
                elif task.design_status == 'open':
                    self.write(cr, uid, task.id, {'design_status': 'done'})
            
            else:
                if task.design_status == 'done':
                    self.write(cr, uid, task.id, {'design_status': 'open'})
                elif task.design_status == 'open':
                    self.write(cr, uid, task.id, {'design_status': 'draft'})
        return True

    def next_status(self, cr, uid, ids, *args):
        return self._change_status(cr, uid, ids, True, *args)

    def prev_status(self, cr, uid, ids, *args):
        return self._change_status(cr, uid, ids, False, *args)

project_project()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
