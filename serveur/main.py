from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import json
from models.host import *
#from models.action import *
from database import configure_db, engine
from sqlmodel import Session, select

async def on_start_up():
    configure_db()

app = FastAPI(on_startup=[on_start_up])

@app.get("/hosts")
def read_hosts() -> list[Host]:
    with Session(engine) as session:
        hosts = session.exec(select(Host)).all()
        return hosts
    
@app.get("/host/{host_id}")
def read_host(host_id: int) -> Host:
    with Session(engine) as session:
        host = session.get(Host, host_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        return host
    
@app.post("/host")
def create_host(host: Host) -> Host:
    with Session(engine) as session:
        session.add(host)
        session.commit()
        session.refresh(host)
        return host
    
@app.delete("/host/{host_id}")
def delete_host(host_id: int) -> dict:
    with Session(engine) as session:
        host = session.get(Host, host_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        session.delete(host)
        session.commit()
        return {"ok": True}

@app.put("/host/{host_id}")
def update_host(host_id: int, updated_host: Host) -> Host:
    with Session(engine) as session:
        host = session.get(Host, host_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        host.name = updated_host.name
        host.ip = updated_host.ip
        session.add(host)
        session.commit()
        session.refresh(host)
        return host