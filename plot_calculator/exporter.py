import pandas as pd


class Exporter:

    @staticmethod
    def export(filepath, outputs):
        writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
        workbook = writer.book
        worksheet = workbook.add_worksheet('Sheet 1')
        writer.sheets['Sheet 1'] = worksheet
        col_num = 0
        for output in outputs:
            output.to_excel(writer, sheet_name='Sheet 1', startrow=0, startcol=col_num, index=False)
            col_num += 3
        writer.save()
