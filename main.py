import openpyxl as xl
from fastapi import FastAPI
from model import Items,StockItems,ExpenseModel
from datetime import datetime
import random


app=FastAPI()



def generate_ids(id_length=6):
    low=10**(id_length-1)
    high=10**(id_length)-1
    return random.randint(low,high)


@app.post("/add_items")
def add_Items(items:Items):
    wb=xl.load_workbook("database.xlsx")
    sheet=wb["Items data"]
    id=generate_ids(6)
    flag=True
    while flag:
        if sheet.max_row==1 and sheet["A1"]==None:
            flag=False
            continue
        for index,val in enumerate(sheet.iter_rows(values_only=True)):
            if val[0]==id:
                id=generate_ids(6)
                continue
            if index==sheet.max_row-1:
                flag=False

    sheet.append([id,items.name,items.price,items.sticks])
    wb.save("database.xlsx")
    wb.close()
    return {
        "id":id,
        "data":items
    }

@app.post("/add_opening_data")
def add_opening_data(data:StockItems):
    wb=xl.load_workbook("database.xlsx")
    sheet=wb[data.type]
    for index,val in enumerate(sheet.iter_rows(values_only=True)):
        if val.__contains__(data.name):
            return {
                "Error":"Duplicated Items"
            }
    sheet.append([data.id,data.name,data.price,data.packs,data.sticks,datetime.now()])

    wb.save("database.xlsx")
    wb.close()
    return data

@app.post("/edit_opening_stock")
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
    id=generate_ids(6)
    flag=True

    while flag:
        if sheet.max_row==1 and sheet["A1"]==None:
            flag=False
            continue
        for index,val in enumerate(sheet.iter_rows(values_only=True)):
            if val[0]==id:
                id=generate_ids(6)
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

@app.post("/")
def calculate_leakage(data:dict):
    online_amount=data["online"]
    cash_amount=data["cash"]
    wb=xl.load_workbook("database.xlsx")
    items=wb["Items data"]
    opening_sheet=wb["Opening Data"]
    closing_sheet=wb["Closing Data"]
    expense_sheet=wb["Expense data"]
    data=[]
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