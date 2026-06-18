from fastapi import APIRouter, HTTPException
from mysql import connector
import database.agent_db
import agent_utiles
from agent_utiles import AgentBody

router = APIRouter()

agent_db = database.agent_db.AgentDB()

@router.post("/agents", status_code = 201)
def create_agent(body:AgentBody) -> dict:
    """docstring"""
    try:
        return agent_db.create_agent(body)

    except agent_utiles.InvalidName as e:
        raise HTTPException(status_code=422, detail= "Name is missing here.")
    
    except agent_utiles.InvalidSpecialty as e:
        raise HTTPException(status_code=422, detail= "specialty missing here.")
    
    except agent_utiles.NoRank as e:
            raise HTTPException(status_code=422, detail= "Rank missing here.")
    
    except agent_utiles.InvalidRank as e:
        raise HTTPException(status_code=400, detail= "Invalid runk.")
    
    except connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Something get wronng with the connection: {e}")

@router.get("/agents")
def get_all_of_agents() -> list:
    """docstring"""
    try:
        return agent_db.get_all_agents()
    
    except connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Something get wronng with the connection: {e}")
    
@router.get("/agents/{id}")
def get_agent_by_id(id:int):
    try:
        agent = agent_db.get_agent_by_id(id)
        if agent:
            return agent
        else:
            raise HTTPException(status_code=404, detail= "The agent did not found")
    
    except connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Something get wronng with the connection: {e}")
    
@router.put("/agents/{id}")
def update_agent(id:int, body:AgentBody):
    """docstring"""
    try:
        is_updated = agent_db.update_agent_handle(id, body)
        if is_updated:
            return {f"The agent {id} is updated successfully"}
        else:
            raise HTTPException(status_code=404, detail= "The agent did not found")
    
    except agent_utiles.InvalidRank as e:
        raise HTTPException(status_code=400, detail= "Invalid runk.")
    
    except agent_utiles.EmptyInput as e:
        raise HTTPException(status_code=400, detail= "Empty body.")
    
    except connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Something get wronng with the connection: {e}")

@router.put("/agents/{id}/deactivate")
def deactivate_agent(id:int):
    """docstring"""
    try:
        return agent_db.deactivate_agent(id)
    
    except agent_utiles.AgentNotFound:
        raise HTTPException(status_code=404, detail= "The agent did not found")
    
    except connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Something get wronng with the connection: {e}")
    
@router.get("/agents/{id}/performance")
def get_agent_performance(id:int):
    """docstring"""
    try:
        return agent_db.get_agent_performance(id)
    
    except agent_utiles.AgentNotFound:
        raise HTTPException(status_code=404, detail= "The agent did not found")
    
    except connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Something get wronng with the connection: {e}")