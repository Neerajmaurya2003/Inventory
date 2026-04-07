import openpyxl as xl
from fastapi import FastAPI
from model import Items,StockItems,ExpenseModel
from datetime import datetime
import random


app=FastAPI()

item_data=[["1","Advance",25,20],["2","Lite",25,20],["3","Gold Flake",12,10],["4","Double Switch",25,10]]




@app.post("/add_items")
def add_Items(item:Items=None):
    wb=xl.load_workbook("database.xlsx")
    sheet=wb["Items data"]
    if sheet.max_row==1:
        for i in item_data:
            sheet.append(i)
            wb.save("database.xlsx")
        wb.close()
        return{
            "message":"Items Updated "
        }
    for i,val in enumerate(sheet.iter_rows(values_only=True)):
        if i==0:
            continue
        if item.name.lower()==val[1].lower():
            return {
                "message":"Duplicated Items"
            }
        item_data.append([str(sheet.max_row),item.name,item.price,item.sticks])
    sheet.append([str(sheet.max_row),item.name,item.price,item.sticks])
    wb.save("database.xlsx")
    wb.close()
    return {
        "message":"Item Saved Successfully",
        "data":{
            "id":sheet.max_row-1,
            "name":item.name,
            "price":item.price,
            "sticks":item.sticks
        }
    }


@app.post("/add_stocks_data")
def add_stock_data(data_list: list[StockItems]):
    wb=xl.load_workbook("database.xlsx")
    sheet=wb["Stock Data"]
    opening_stock=[]
    opening_balance=0
    closing_balance=0
    for i, val in enumerate(sheet.iter_rows(values_only=True)):
        if i==0: continue
        opening_stock.append(list(val))
        opening_balance +=((val[3]*val[5])+val[4])*val[2]
    for data in data_list:
        closing_balance += ((data.packs*data.stick_count)+data.sticks)*data.price

    sheet2=wb["Credit"]
    sheet2.append([datetime.now(),opening_balance,closing_balance,opening_balance-closing_balance])
    wb.save("database.xlsx")
    wb.close()
    return {
        "opening Balance":opening_balance,
        "Closing Balance":closing_balance,
        "Profit Loss":opening_balance-closing_balance
    }

@app.post("/edit_stocks")
def edit_opening_stock(data:StockItems):
    wb=xl.load_workbook("database.xlsx")
    sheet=wb[data.type]

    for idx,row in enumerate(sheet.iter_rows(values_only=True)):
        if row[0]==data.name:
            sheet.cell(row=idx+1,column=2).value=data.price
            sheet.cell(row=idx+1,column=3).value=data.packs
            sheet.cell(row=idx+1,column=4).value=data.sticks
            sheet.cell(row=idx+1,column=5).value=datetime.now()
            wb.save("database.xlsx")
            return {
                "name":data.name,
                "price":data.price,
                "packs":data.packs,
                "sticks":data.sticks
            }
            

    
    wb.close()
    return{
        "message":"Entry not found"
    }


@app.post("/add_expense")
def add_expense(data:ExpenseModel):
    wb=xl.load_workbook("database.xlsx")
    sheet=wb["Expense data"]
    id=89
    flag=True

    while flag:
        if sheet.max_row==1 and sheet["A1"]==None:
            flag=False
            continue
        for index,val in enumerate(sheet.iter_rows(values_only=True)):
            if val[0]==id:
                id=89
                continue
            if index==sheet.max_row-1:
                flag=False
    
    sheet.append([id,data.name,data.type,data.amount,datetime.now()])


@app.post("/add_new_stock")
def add_new_stock(list:list[StockItems]):
    wb=xl.load_workbook("database.xlsx")
    sheet=wb[list[0].type]
    for data in list:
        for i,val in enumerate(sheet.iter_rows(values_only=True)):
            if val[0]==data.id:
                sheet.cell(row=i+1,column=4).value=val[3]+data.packs
                wb.save("database.xlsx")
                continue

    wb.close()
    pass

@app.post("/calculate_leakage")
def calculate_leakage(data:dict):
    online_amount=data["online"]
    cash_amount=data["cash"]
    wb=xl.load_workbook("database.xlsx")
    items=wb["Items data"]
    opening_sheet=wb["Opening Data"]
    closing_sheet=wb["Closing Data"]
    expense_sheet=wb["Expense data"]
    opening_balance=0
    closing_balance=0
    total_expense=0

    for i,val in enumerate(expense_sheet.iter_rows(values_only=True)):
        if i==0:
            continue
        total_expense+=val[3]

    for i, val in enumerate(items.iter_rows(values_only=True)):
        if i==0:
            continue
        id=val[0]
        stick_count=val[2]
        price=val[3]

        for j, value in enumerate(opening_sheet.iter_rows(values_only=True)):
            if j==0:
                continue
            total_stick_count=0
            if value[0]==id:
               total_stick_count= (value[3]*stick_count)+value[4]
               opening_balance += total_stick_count*price
            
        for j, value in enumerate(closing_sheet.iter_rows(values_only=True)):
            if j==0:
                continue
            total_stick_count=0
            if value[0]==id:
               total_stick_count= (value[3]*stick_count)+value[4]
               closing_balance +=total_stick_count*price

    wb.close()
    return{
        "opening Balance":opening_balance,
        "Closing Balance":closing_balance,
        "Total Expenses":total_expense,
        "Total Earning":opening_balance-closing_balance,
        "total amount Earned":online_amount+ cash_amount,
        "Profit/Loss":(opening_balance-closing_balance)-(online_amount+ cash_amount)
    }