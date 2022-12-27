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
        CPs = []
        MEs = []
        names = [] 
        costs = []
        bounds = []
        sum_mat = []
        # print(data['data'])
        row = data['data']

        for i in range(len(row)):
            print(row[i])
            sum_mat.append(1)
            names.append(row[i]['name'])
            costs.append(row[i]['cost'])
            CPs.append(row[i]['CP'])
            MEs.append(row[i]['ME'])
            bounds.append((row[i]['min'], row[i]['max']))
        
        CPs = [ -x for x in CPs]
        MEs = [ -x for x in MEs]

        # inputs_matrix = [CPs, MEs]
        print("CP: ", CPs)
        print("ME: ", MEs)
        print("Names: ", names)
        print("Costs: ", costs)
        print("Bounds: ", bounds)
        print("Sum matrix: ", sum_mat)

        # print(inputs_matrix)

        res = linprog(costs, A_ub=[CPs, MEs], b_ub=[-16, -2200], A_eq=[sum_mat], b_eq=[1] #, bounds=bounds
        )
        # res = linprog(data['cost'], A_eq=data['ing_comp'], b_eq=data['req_ing'])
        print(res)

        f = dict()
        r_items = res.items()
        for k, v in r_items:
            if str(type(v)) == "<class 'numpy.ndarray'>":
                # print("Found")
                f.update({k:list(v)})
            else: 
                # print(type(v))
                f[k] = str(v)

        res_dict = {
            "quantities": list(res.x),
            "input": item, 
            # "raw": f
        }

        return res_dict

    except:
        return {"error": "Some Error occured"}
