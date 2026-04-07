import openpyxl as xl


wb=xl.load_workbook("database.xlsx")
sheet=wb.sheetnames

print(sheet)