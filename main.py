from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import json
from functools import wraps
from monitor import *

## ANCIEN CODE AVANT LA BASE DE DONNEES AVEC JSON, A GARDER POUR REFERENCE ##

def load_datas(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global datas
        with open('datas.json', 'r', encoding='utf-8') as file:
            datas = json.load(file)
        return func(*args, **kwargs)
    return wrapper

def write_datas():
    with open('datas.json', 'w', encoding='utf-8') as file:
        json.dump(datas, file, indent=4)


app = FastAPI()

# Un icon pour plus de style
@app.get('/favicon.ico', include_in_schema=False)
async def favicon(): return FileResponse('favicon.ico')

@app.get("/ordinateurs")
@load_datas
def read_root() -> list[object]:
    return datas

@app.get("/ordinateur/{id:int}")
@load_datas
def read_root(id) -> object:
    if id >= len(datas): raise HTTPException(status_code=404, detail="Cet ordinateur n'existe pas")
    return datas[id]

@app.get("/ordinateur/{id:int}/cpu")
@load_datas
def read_root(id) -> Cpu:
    if id >= len(datas): raise HTTPException(status_code=404, detail="Cet ordinateur n'existe pas")
    return datas[id]['cpu']

@app.get("/ordinateur/{id:int}/memory")
@load_datas
def read_root(id) -> Memory:
    if id >= len(datas): raise HTTPException(status_code=404, detail="Cet ordinateur n'existe pas")
    return datas[id]['memory']

@app.get("/ordinateur/{id:int}/network_interfaces")
@load_datas
def read_root(id) -> list[NetworkInterface]:
    if id >= len(datas): raise HTTPException(status_code=404, detail="Cet ordinateur n'existe pas")
    return datas[id]['network_interfaces']

@app.get("/ordinateur/{id:int}/network_interfaces/{interface_id:int}")
@load_datas
def read_root(id,interface_id) -> NetworkInterface:
    if id >= len(datas): raise HTTPException(status_code=404, detail="Cet ordinateur n'existe pas")
    if interface_id >= len(datas[id]['network_interfaces']): raise HTTPException(status_code=404, detail="Cette interface n'existe pas")
    return datas[id]['network_interfaces'][interface_id]

@app.get("/ordinateur/{id:int}/network_interfaces/{interface_id:int}/ip_addresses")
@load_datas
def read_root(id,interface_id) -> list[IPAddress]:
    if id >= len(datas): raise HTTPException(status_code=404, detail="Cet ordinateur n'existe pas")
    if interface_id >= len(datas[id]['network_interfaces']): raise HTTPException(status_code=404, detail="Cette interface n'existe pas")
    return datas[id]['network_interfaces'][interface_id]['ip_addresses']

@app.get("/ordinateur/{id:int}/network_interfaces/{interface_id:int}/mac_addresses")
@load_datas
def read_root(id,interface_id) -> list[MacAddress]:
    if id >= len(datas): raise HTTPException(status_code=404, detail="Cet ordinateur n'existe pas")
    if interface_id >= len(datas[id]['network_interfaces']): raise HTTPException(status_code=404, detail="Cette interface n'existe pas")
    return datas[id]['network_interfaces'][interface_id]['mac_addresses']

@app.get("/ordinateur/{id:int}/disk")
@load_datas
def read_root(id) -> list[Disk]:
    if id >= len(datas): raise HTTPException(status_code=404, detail="Cet ordinateur n'existe pas")
    return datas[id]['disk']

@app.get("/ordinateur/{id:int}/disk/{disk_id:int}")
@load_datas
def read_root(id,disk_id) -> Disk:
    if id >= len(datas): raise HTTPException(status_code=404, detail="Cet ordinateur n'existe pas")
    if disk_id >= len(datas[id]['disk']): raise HTTPException(status_code=404, detail="Ce disque n'existe pas")
    return datas[id]['disk'][disk_id]

@app.get("/ordinateur/{id:int}/disk/{disk_id:int}/partitions")
@load_datas
def read_root(id,disk_id) -> list[Partition]:
    if id >= len(datas): raise HTTPException(status_code=404, detail="Cet ordinateur n'existe pas")
    if disk_id >= len(datas[id]['disk']): raise HTTPException(status_code=404, detail="Ce disque n'existe pas")
    return datas[id]['disk'][disk_id]['partitions']

@app.post("/ordinateur/{id:int}/refresh")
@load_datas
def read_root(id) -> dict[str, str]:
    if id >= len(datas): raise HTTPException(status_code=404, detail="Cet ordinateur n'existe pas")
    ordinateur = Ordinateur()
    datas[id] = ordinateur.model_dump()
    write_datas()
    return {"status": "success"}