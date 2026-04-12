import os
from fastapi import FastAPI
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import json

load_dotenv()

app=FastAPI()


MONGO_URI=os.getenv("MONGO_URI","")


assert MONGO_URI, ValueError


client=MongoClient(MONGO_URI)

db=client["inventory"]

def retrive_item_list():
    collection=db["item-list"]
    try:
        if collection.find():
            data_list=collection.find().to_list()
            for data in data_list:
                print(data)
            return  {
                "data":data_list,
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

response=retrive_item_list()

print(response)