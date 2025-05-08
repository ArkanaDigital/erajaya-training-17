from odoo import models

class PartnerXlsx(models.AbstractModel):
    _name = 'report.agnes_academy_report.report_name'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        for obj in partners:
            report_name = obj.name
            # One sheet by partner
            sheet = workbook.add_worksheet(report_name[:31])
            bold = workbook.add_format({'bold': True})
            sheet.write(0, 0, obj.name, bold)
            sheet.write(1, 0, 'ID', bold)
            sheet.write(1, 1, 'Name', bold)
            sheet.write(1, 2, 'Email', bold)
            sheet.write(1, 3, 'Phone', bold)
            sheet.write(1, 4, 'Street', bold)
            sheet.write(1, 5, 'City', bold)

            # sheet.insert_image('B20', '/web/arkana_academy_report/description/odoo_icon.png')

            sheet.set_column('A:A', 15)
            sheet.set_column('B:B', 30)
            sheet.set_column('C:C', 30)
            sheet.set_column('D:D', 15)
            sheet.set_column('E:E', 30)
            sheet.set_column('F:F', 20)
            sheet.set_column('G:G', 20)
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            for col_num, value in enumerate(['ID', 'Name', 'Email', 'Phone', 'Street', 'City', 'Country']):
                sheet.write(1, col_num, value, header_format)
            sheet.write(1, 6, 'Country', bold)

            row = 2
            for partner in partners:
                sheet.write(row, 0, partner.id)
                sheet.write(row, 1, partner.name)
                sheet.write(row, 2, partner.email or '')
                sheet.write(row, 3, partner.phone or '')
                sheet.write(row, 4, partner.street or '')
                sheet.write(row, 5, partner.city or '')
                sheet.write(row, 6, partner.country_id.name if partner.country_id else '')
                row += 1
