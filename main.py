from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
# for feed formulation
from scipy.optimize import linprog
from fastapi.responses import JSONResponse
import json
from fastapi.encoders import jsonable_encoder

class Item(BaseModel):
    cost: list = []
    ing_comp: list = []
    req_ing: list = []
    data: list = []

class ResModel(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


app = FastAPI()

# @app.post("/formulate/", response_model=ResItem)
@app.post("/formulate/")
async def formulate_feed(item: Item):
    try:
        data = item.dict()
        res = linprog(data['cost'], A_eq=data['ing_comp'], b_eq=data['req_ing'])
        # print(res)

        f = dict()
        r_items = res.items()
        for k, v in r_items:
            if str(type(v)) == "<class 'numpy.ndarray'>":
                print("Found")
                f.update({k:list(v)})
            else: 
                print(type(v))
                f[k] = str(v)

        res_dict = {
            "input": item, 
            "quantities": list(res.x),
            "raw": f
        }

        return res_dict

    except:
        return {"error": "Some Error occured"}
