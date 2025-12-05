from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Mes propres modèles customs
from models.host import *
from models.action import *
from models.indicator import *
from models.indicator_values import *

# Gestion de la base de données
from database import configure_db, engine
from sqlmodel import SQLModel, Session, select

# Autres import utils
import asyncio
import datetime
from tools.password_security import chiffrer_mot_de_passe


async def execute_indicator(indicator: Indicator) -> None:
    with Session(engine) as session:
        action = session.get(Action, indicator.action_id)
        if not action: return "Action de l'indicateur not found"
        try:
            indicator_host = session.get(Host, indicator.host_id)
            value, unite, error_message = action.exec_script(host=indicator_host, parametre=indicator.parametre)
            indicator_value = IndicatorValue(indicator_id=indicator.id, value=value, unite=unite, error_message=error_message)
            session.add(indicator_value)
            session.commit()
            session.refresh(indicator_value)
        except Exception as e:
            print(f"Erreur dans l'indicateur {indicator.id}: {e}")

async def scheduler():
    while True:
        with Session(engine) as session:
            indicators = session.exec(select(Indicator)).all()
            for indicator in indicators:
                last = session.exec(select(IndicatorValue).where(IndicatorValue.indicator_id == indicator.id)
                    .order_by(IndicatorValue.date.desc()).limit(1)).first()
                if not last or (datetime.datetime.utcnow() - last.date) >= datetime.timedelta(seconds=indicator.interval):
                    await execute_indicator(indicator)
        await asyncio.sleep(10)

async def start_scheduler():
    asyncio.create_task(scheduler())



## Gestion de la partie base de données au démarrage de l'application ##
async def on_start_up():
    pass
    configure_db()

app = FastAPI(on_startup=[on_start_up, start_scheduler]) ## Initialisation de l'application FastAPI ##

origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

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
        host.password = chiffrer_mot_de_passe(host.password) if host.password else None
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
        host.name = updated_host.name if updated_host.name else host.name
        host.ip = updated_host.ip if updated_host.ip else host.ip
        host.username = updated_host.username if updated_host.username else host.username
        if updated_host.password:
            host.password = chiffrer_mot_de_passe(updated_host.password)
        host.ssh_port = updated_host.ssh_port if updated_host.ssh_port else host.ssh_port
        session.add(host)
        session.commit()
        session.refresh(host)
        return host

@app.get("/actions")
def get_actions() -> list[Action]:
    with Session(engine) as session:
        actions = session.exec(select(Action)).all()
        return actions
    
@app.get("/action/{action_id}")
def get_action(action_id: int) -> Action:
    with Session(engine) as session:
        action = session.get(Action, action_id)
        if not action: raise HTTPException(status_code=404, detail="Action not found")
        return action
    
@app.post("/action")
def create_action(action: Action) -> Action:
    with Session(engine) as session:
        session.add(action)
        session.commit()
        session.refresh(action)
        return action
    
@app.delete("/action/{action_id}")
def delete_action(action_id: int) -> dict:
    with Session(engine) as session:
        action = session.get(Action, action_id)
        if not action: raise HTTPException(status_code=404, detail="Action not found")
        session.delete(action)
        session.commit()
        return {"ok": True}
    
@app.put("/action/{action_id}")
def update_action(action_id: int, updated_action: Action) -> Action:
    with Session(engine) as session:
        action = session.get(Action, action_id)
        if not action: raise HTTPException(status_code=404, detail="Action not found")
        action.name = updated_action.name if updated_action.name else action.name
        action.script_path = updated_action.script_path if updated_action.script_path else action.script_path
        action.min_value = updated_action.min_value if updated_action.min_value is not None else action.min_value
        action.max_value = updated_action.max_value if updated_action.max_value is not None else action.max_value
        action.ssh_error_default_value = updated_action.ssh_error_default_value if updated_action.ssh_error_default_value is not None else action.ssh_error_default_value
        action.unite = updated_action.unite if updated_action.unite else action.unite
        action.rounding = updated_action.rounding if updated_action.rounding is not None else action.rounding
        session.add(action)
        session.commit()
        session.refresh(action)
        return action
    



### Endpoints pour les indicateurs ###
@app.get("/host/{host_id}/indicators")
def get_host_indicators(host_id: int) -> list[IndicatorWithLastValue]:
    with Session(engine) as session:
        indicators = session.exec(select(Indicator).where(Indicator.host_id == host_id)).all()
        result_liste = []
        for indicator in indicators:
            last_value = session.exec(select(IndicatorValue).where(IndicatorValue.indicator_id == indicator.id).order_by(IndicatorValue.date.desc()).limit(1)).first()
            result_liste.append(IndicatorWithLastValue(**indicator.model_dump(), last_value=last_value))
        return result_liste
    
@app.post("/host/{host_id}/indicator")
def create_host_indicator(host_id: int, indicator: Indicator) -> Indicator:
    with Session(engine) as session:
        indicator.host_id = host_id
        session.add(indicator)
        session.commit()
        session.refresh(indicator)
        return indicator
    
@app.delete("/indicator/{indicator_id}")
@app.delete("/host/{host_id}/indicator/{indicator_id}")
def delete_indicator(indicator_id: int, host_id: int = None) -> dict:
    with Session(engine) as session:
        indicator = session.get(Indicator, indicator_id)
        if not indicator: raise HTTPException(status_code=404, detail="Indicator not found")
        session.delete(indicator)
        session.commit()
        return {"ok": True}
    
@app.post("/indicator/{indicator_id}/execute")
@app.post("/host/{host_id}/indicator/{indicator_id}/execute")
def execute_indicator_action(indicator_id: int, host_id: int = None) -> bool:
    with Session(engine) as session:
        indicator = session.get(Indicator, indicator_id)
        if not indicator: raise HTTPException(status_code=404, detail="Indicator not found")
        host = session.get(Host, indicator.host_id)
        if not host: raise HTTPException(status_code=404, detail="Host not found")
        action = session.get(Action, indicator.action_id)
        if not action: raise HTTPException(status_code=404, detail="Action not found for this indicator")
        try:
            value, unite, error_message = action.exec_script(host=host, parametre=indicator.parametre)
            indicator_value = IndicatorValue(indicator_id=indicator.id, value=value, unite=unite, error_message=error_message)
            session.add(indicator_value)
            session.commit()
            session.refresh(indicator_value)
            return True
        except Exception as e:
            print(f"Erreur lors de l'exécution de l'indicateur {indicator_id}: {e}")
            return False
        
@app.get("/host/{host_id}/indicator/{indicator_id}/values")
@app.get("/indicator/{indicator_id}/values")
def get_indicator_values(indicator_id: int, host_id: int = None) -> ListeIndicatorValue:
    with Session(engine) as session:
        indicator = session.get(Indicator, indicator_id)
        action = session.get(Action, indicator.action_id)
        if not indicator or (host_id and indicator.host_id != host_id):
            raise HTTPException(status_code=404, detail="Indicator not found for this host")
        values = session.exec(select(IndicatorValue).where(IndicatorValue.indicator_id == indicator_id).order_by(IndicatorValue.date)).all()
        return ListeIndicatorValue(values=values, action_min_value=action.min_value, action_max_value=action.max_value, action_unite=action.unite)
    
@app.delete("/host/{host_id}/indicator/{indicator_id}/values")
@app.delete("/indicator/{indicator_id}/values")
def purge_indicator_values(indicator_id: int, host_id: int = None) -> dict:
    with Session(engine) as session:
        indicator = session.get(Indicator, indicator_id)
        if not indicator:
            raise HTTPException(status_code=404, detail="Indicator not found")
        if host_id and indicator.host_id != host_id:
            raise HTTPException(status_code=404, detail="Indicator not found for this host")
        values = session.exec(select(IndicatorValue).where(IndicatorValue.indicator_id == indicator_id)).all()
        for value in values:
            session.delete(value)
        session.commit()
        return {"ok": True}