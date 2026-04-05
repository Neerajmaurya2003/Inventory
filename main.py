import openpyxl as xl
from fastapi import FastAPI
import json
from model import Items,StockItems
from datetime import datetime

# wb=xl.load_workbook("database.xlsx")

# list=["Items data","Expense data", "Opening Data","Closing Data","Credit "]
# for i in list:
#     wb.create_sheet(i)

# wb.save("database.xlsx")

app=FastAPI()

@app.post("/add_items")
def add_Items(items:Items):

    wb=xl.load_workbook("database.xlsx")
    sheet=wb["Items data"]
    sheet.append([items.name,items.price,items.stick_count])
    wb.save("database.xlsx")
    wb.close()
    return items

@app.post("/add_opening_data")
def add_opening_data(data:StockItems):
    wb=xl.load_workbook("database.xlsx")
    sheet=wb["Opening Data"]
    for i in sheet.iter_rows(values_only=True):
        if i.__contains__(data.name):
            return {
                "Error":"Duplicated Items"
            }
    sheet.append([data.name,data.price,data.packs,data.sticks,datetime.now()])

    wb.save("database.xlsx")
    wb.close()
    return data

@app.post("/edit_opening_stock")
def edit_opening_stock(data:StockItems):
    wb=xl.load_workbook("database.xlsx")
    sheet=wb["Opening Data"]

    for idx,row in enumerate(sheet.iter_rows(values_only=True)):
        if row[0]==data.name:
            sheet.cell(row=idx,column=2,value=data.price)
            sheet.cell(row=idx,column=2,value=data.packs)
            sheet.cell(row=idx,column=2,value=data.sticks)
            sheet.cell(row=idx,column=2,value=datetime.now())
            return{
                "message":"Sheet Updated"
            }

    wb.save("database.xlsx")
    wb.close()
    return{
        "message":"Entry not found"
    }