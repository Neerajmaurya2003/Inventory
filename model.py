from pydantic import BaseModel


class Items(BaseModel):
    name:str
    price:int
    stick_count:int

class StockItems(BaseModel):
    name:str
    price:int
    packs:int
    sticks:int
    pass



