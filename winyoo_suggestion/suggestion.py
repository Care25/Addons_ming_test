# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions, _
from duplicity.tempdir import default
_STATES = [
    ('draft', 'Draft'),
    ('submitted', 'แจ้งแล้ว'),
    ('received', 'คนที่เกี่ยวข้องรับเรื่อง'),
    ('done', 'เสร็จแล้ว')
]

class Suggestion(models.Model):
    _name= 'suggestion'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    @api.model
    def _get_default_name(self):
        return self.env['res.users'].browse(self.env.uid)
#     _track = {
#         'state': {
#             'suggestion.mt_suggestion_to_approve': 
#                 (lambda self, cr, uid, obj,
#                 ctx=None: obj.state == 'submitted'),
#             'suggestion.mt_suggestion_approved':
#                 (lambda self, cr, uid, obj,
#                 ctx=None: obj.state == 'received'),
#             'suggestion.mt_suggestion_done':
#                 (lambda self, cr, uid, obj,
#                 ctx=None: obj.state == 'done'),
#         },
#     }
    
    main_suggest = fields.Selection([('program','แจ้งแก้ไขโปรแกรม'),('car','ร้องเรียนกระบวนการที่ไม่เป็นไปตามข้อตกลง'),('ask','คำถามเกี่ยวกับโปรแกรมและกระบวนการ')
                                ,('report','แจ้งแก้ไขเอกสาร'),('idea','แนะนำและเสนอข้อคิดเห็นเกี่ยวกับงาน')],track_visibility='onchange')
    functional = fields.Selection([('sale','งานขาย'),
                    ('purchase','งานจัดซื้อ'),
                    ('warehouse','งานคลังสินค้า'),
                    ('delivery','งานจัดส่ง'),
                    ('account','งานเอกสารบัญชี/การเงิน'),
                    ('hr','งานบุคคล'),
                    ('others','งานอื่นๆ')],track_visibility='onchange')
    
    found_date = fields.Date(default = fields.Date.today(),
                             track_visibility='onchange')
    name = fields.Many2one('res.users', size=32, required=True,
                       default=_get_default_name,
                       track_visibility='onchange')
    manager = fields.Many2one('res.users', size=32,
                              track_visibility='onchange')
    note = fields.Text('Detail', size=32,
                       track_visibility='onchange')
    state = fields.Selection(selection=_STATES,
                             string='Status',
                             required=True,
                             default='draft',
                             track_visibility='onchange')  


#     @api.multi
#     def button_suggestion(self):
#         print "------------------------------------------------------------------"
#         print "self.env = ", self.env
#         print "self.env.user = ", self.env.user
#         print "self.env.user.name = ", self.env.user.name
#         print "self.env.cr = ", self.env.cr
#         print "------------------------------------------------------------------" 
    
    
        
    @api.multi
    def button_draft(self):
        self.state = 'draft'
        return True

    @api.multi
    def button_submitted(self):
        self.state = 'submitted'
        a = ""
        if self.main_suggest:
            if self.main_suggest == "program":
                a = r"มีผู้แจ้งหัวข้อ:: แจ้งแก้ไขโปรแกรม" +"<br />" + r" รายละเอียด:: " + str(self.note)
            if self.main_suggest == 'car':
                a = r"มีผู้แจ้งหัวข้อ:: ร้องเรียนกระบวนการที่ไม่เป็นไปตามข้อตกลง" +"<br />" + r" รายละเอียด:: " + str(self.note)
            if self.main_suggest == 'ask':
                a = r"มีผู้แจ้งหัวข้อ:: คำถามเกี่ยวกับโปรแกรมและกระบวนการ" +"<br />" + r" รายละเอียด:: " + str(self.note)
            if self.main_suggest == 'report':
                a = r"มีผู้แจ้งหัวข้อ:: แจ้งแก้ไขเอกสาร" +"<br />" + r" รายละเอียด:: " + str(self.note)
            if self.main_suggest == 'idea':
                a = r"มีผู้แจ้งหัวข้อ:: แนะนำและเสนอข้อคิดเห็นเกี่ยวกับงาน" +"<br />" + r" รายละเอียด:: " + str(self.note)
        self.message_post( body= a, subtype='mt_comment') 
        return True

    @api.multi
    def button_received(self):
        self.state = 'received'
        return True
        
    @api.multi
    def button_done(self):
        self.state = 'done'
     
#     @api.onchange('state')
#     def auto_sent(self):
#        if self.state in ["submitted"]:
#         msg= _("Dear User: your account has been update")
#         return self.message_post(body=msg) 
     
     
    @api.model
    def create(self, vals):
        if vals.get('manager'):
            name = self.env['res.users'].browse(vals.get(
                'manager'))
            vals['message_follower_ids'] = [(4, name.partner_id.id)]
        return super(Suggestion, self).create(vals)
 
    @api.multi
    def write(self, vals):
        self.ensure_one()
        if vals.get('manager'):
            name = self.env['res.users'].browse(
                vals.get('manager'))
            vals['message_follower_ids'] = [(4, name.partner_id.id)]
        res = super(Suggestion, self).write(vals)
        return res
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: