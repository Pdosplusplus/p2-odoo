# -*- encoding: utf-8 -*-

from openerp.report import report_sxw
from openerp.osv import osv

class report_scf (report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(report_scf, self).__init__(cr, uid, name, context)

class report_client(osv.AbstractModel):

    #Nombre del objeto
    _name="report.scf.client"

    #De quien hereda esta clase
    _inherit="report.abstract_report"


    _template="scf.client"

    #Nombre de la class que hereda de report_sxw.rml_parse
    _wrapped_report_class=report_scf

