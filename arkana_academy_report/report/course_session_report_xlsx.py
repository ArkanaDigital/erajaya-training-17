from odoo import models

class CourseSessionXlsx(models.AbstractModel):
    _name = 'report.arkana_academy_report.course_session_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Course Session Report (XLSX)'

    # def generate_xlsx_report(self, workbook, data, partners):
    #     for obj in partners:
    #         report_name = obj.name
    #         # One sheet by partner
    #         sheet = workbook.add_worksheet(report_name[:31])
    #         bold = workbook.add_format({'bold': True})
    #         sheet.write(0, 0, obj.name, bold)

    def generate_xlsx_report(self, workbook, data, sessions):
        # Format definitions
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 12,
            'bg_color': '#f2f2f2',
            'border': 1
        })
        
        cell_format = workbook.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'border': 1
        })
        
        number_format = workbook.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '#,##0'
        })
        
        percentage_format = workbook.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'num_format': '0.00%'
        })

        date_format = workbook.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'border': 1,
            'num_format': 'dd/mm/yyyy'
        })

        # Process each session
        for session in sessions:
            # Create worksheet
            sheet = workbook.add_worksheet(session.name[:31])  # Excel limits sheet names to 31 chars
            sheet.set_column('A:A', 5)   # No
            sheet.set_column('B:B', 30)  # Name
            sheet.set_column('C:E', 15)  # Other columns
            
            # Write headers
            headers = [
                'No',
                'Session Name',
                'Start Date',
                'Duration',
                'Seats',
                'Instructor',
                'Course',
                'Status',
                'Occupancy',
            ]
            for col, header in enumerate(headers):
                sheet.write(0, col, header, header_format)

            # Write session info
            row = 1
            sheet.write(row, 0, 1, number_format)
            sheet.write(row, 1, session.name, cell_format)
            sheet.write(row, 2, session.start_date, date_format)
            sheet.write(row, 3, session.duration, number_format)
            sheet.write(row, 4, session.seat_total, number_format)
            sheet.write(row, 5, session.partner_id.name, cell_format)
            sheet.write(row, 6, session.course_id.name, cell_format)
            sheet.write(row, 7, dict(session._fields['state'].selection).get(session.state), cell_format)
            sheet.write(row, 8, session.seat_occupied/100, percentage_format)

            # Add Attendees section
            row += 3
            attendee_headers = [
                'No',
                'Name',
                'Email',
                'Phone',
                'Company'
            ]
            
            sheet.merge_range(row, 0, row, len(attendee_headers)-1, 'Attendees', header_format)
            row += 1
            
            for col, header in enumerate(attendee_headers):
                sheet.write(row, col, header, header_format)
            
            row += 1
            for idx, attendee in enumerate(session.attendee_ids, 1):
                sheet.write(row, 0, idx, number_format)
                sheet.write(row, 1, attendee.name, cell_format)
                sheet.write(row, 2, attendee.email or '', cell_format)
                sheet.write(row, 3, attendee.phone or '', cell_format)
                sheet.write(row, 4, attendee.parent_id.name or '', cell_format)
                row += 1

            # Add summary section
            row += 2
            sheet.merge_range(row, 0, row, 1, 'Summary', header_format)
            row += 1
            
            summary_data = [
                ('Total Seats', session.seat_total),
                ('Occupied Seats', len(session.attendee_ids)),
                ('Available Seats', session.seat_total - len(session.attendee_ids)),
                ('Occupancy Rate', session.seat_occupied/100),
            ]
            
            for label, value in summary_data:
                sheet.write(row, 0, label, cell_format)
                if isinstance(value, float) and label == 'Occupancy Rate':
                    sheet.write(row, 1, value, percentage_format)
                else:
                    sheet.write(row, 1, value, number_format)
                row += 1