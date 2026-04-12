
from datetime import datetime

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


MONGO_URI=os.getenv("MONGO_URI","")


assert MONGO_URI, ValueError


client=MongoClient(MONGO_URI)

db=client["inventory"]


def add_item_list(data_list:list[dict]):
    collection=db["item-list"]
    try:
        collection.insert_many(data_list)
        return{
            "message":"Items Successfully Added"
        }
    except Exception as e:
        return{
            "message":"Something went Wrong",
            "error":e
        }
    
def retrive_item_list():
    collection=db["item-list"]
    try:
        if collection.find():
            for data in collection.find():
                print(data)
            return {
                "data":collection.find().to_list(),
                "message":"Itemss successfully fetched"
            }
        return {
            "message":"Collection is Empty"
        }
    except Exception as e:
        return {
            "message":"Something Went Wrong",
            "error":e
        }

def add_opening_stock(data_list:list[dict]):
    collection=db["opening stock"]
    try:
        collection.insert_many(data_list)
        return {
            "message":"Items added successfully"
        }
    except Exception as e:
        return {
            "message":"Something went Wrong",
            "error":e
        }

def retrive_opening_data():
    collection=db["opening stock"]
    try:
        if collection.find():
            return {
                "data":collection.find().to_list(),
                "message":"Opening Stock Data Retrived Successfully"
            }
        return{
            "message":"Collection is Empty"
        }
    except Exception as e:
        return{
            "message":"Something went Wrong",
            "error":e
        }

def update_opening_stock(data_list:list[dict]):
    collection=db["opening stock"]
    try:
        for data in data_list:
            if collection.find({"data_id":data["data_id"]}):
                collection.update_one({"data_id":data["data_id"]},{"$set":{"packs":data["packs"],"stick_count":data["stick_count"]}})
        return {
                    "message":"Item Updated Successfully"
                }
    except Exception as e:
        return{
            "message":"Something Went Wrong",
            "error":e
        }

def add_daily_stock_data(data:list[dict]):
    collection=db["stock data"]
    try:
        collection.insert_many(data)
        return{
            "data":data,
            "message":"Item Successfully Added"
        }
    except Exception as e:
        return {
            "message":"Something Went Wrong",
            "error":e
        }
    
def calculate_leakage(data:dict):
    collection=db["opening stock"]
    item_collection=db["item-list"]
    try:
        item_list=item_collection.find().to_list()
        opening_data=collection.find().to_list()
        online_income=data["online"]
        cash_income=data["cash"]
        closing_data=data["data list"]
        opening_balance=0
        closing_balance=0
        add_daily_stock_data(closing_data)
        for i in opening_data:
            for j in item_list:
                if i["item_id"]==j["item_id"]:
                    total_sticks=(i["packs"]*j["stick_count"])+i["stick_count"]
                    amount=total_sticks*j["Price"]
                    opening_balance+=amount
        for i in closing_data:
            for j in item_list:
                if i["item_id"]==j["item_id"]:
                    total_sticks=(i["packs"]*j["stick_count"])+i["stick_count"]
                    amount=total_sticks*j["Price"]
                    closing_balance+=amount
        total_income=cash_income+online_income
        update_opening_stock(closing_data)
        predicted_earning=opening_balance-closing_balance
        difference=predicted_earning-total_income
        return{
            "opening balance":opening_balance,
            "closing balance":closing_balance,
            "cash income":cash_income,
            "online Income":online_income,
            "profit/Loss":difference,
            "total income":total_income,
            "predicted income":predicted_earning
        }
    except Exception as e:
        return{
            "message":"Something Went Wrong",
            "error":e
        }




data={
    "online":3200,
    "cash":2000,
    "data list":[
        {
            "item_id":"001",
            "name":"Advance",
            "packs":1,
            "stick_count":6,
            "timestamp":datetime.now()
            
        },
        {
            "item_id":"002",
            "name":"Advance compact",
            "packs":10,
            "stick_count":9,
            "timestamp":datetime.now()
            
        }
    ]

}

response=calculate_leakage(data)
print(response)