from pydantic import BaseModel
from datetime import datetime as dt
from typing import Optional

class Items(BaseModel):
    name:str
    price:int
    sticks:int

class StockItems(BaseModel):
    id:int
    name:str
    price:Optional[int]=None
    packs:int
    sticks:Optional[int]=0
    stick_count:int
    date: Optional[dt]=None


class ExpenseModel(BaseModel):
    name:str
    type:str
    amount:int
    date:Optional[dt]=None


    


