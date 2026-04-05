import openpyxl as xl

# Temporary File to Clear Worksheet

wb=xl.load_workbook("database.xlsx")


sheet = wb["Opening Data"]

sheet.delete_rows(1, sheet.max_row)

wb.save("database.xlsx")
wb.close()