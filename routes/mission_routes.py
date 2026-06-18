from fastapi import APIRouter, HTTPException
from mysql import connector
import database.mission_db
import database.agent_db
import mission_utiles
import agent_utiles

router = APIRouter()

mission_db = database.mission_db.MissionDB()

agent_db = database.agent_db.AgentDB()

@router.post("/missions")
def create_mission(body:mission_utiles.MissionCreateBody):
    """docstring"""
    try:
        return mission_db.create_mission(body)
    
    except mission_utiles.InvalidDifficultyOrImportance:
        raise HTTPException(status_code=400, detail="Invalid difficulty or importance")
    
    except connector.Error:
        raise HTTPException(status_code=500, detail=f"Something get wronng with the connection")
    
@router.get("/missions")
def get_all_missions():
    """docstring"""
    try:
        return mission_db.get_all_missions()
    
    except connector.Error:
        raise HTTPException(status_code=500, detail=f"Something get wronng with the connection")
    
@router.get("/missions/{id}")
def get_mission_by_id(id:int):
    """docstring"""
    try:
        mission = mission_db.get_mission_by_id(id)
        if mission:
            return mission
        else:
            raise HTTPException(status_code=404, detail= "The mission did not found")
    
    except connector.Error:
        raise HTTPException(status_code=500, detail=f"Something get wronng with the connection")
    
@router.put("/missions/{id}/assign/{agent_id}")
def assingn_mission(id:int, agent_id:int):
    """docstring"""
    try:
        open_missions = mission_db.get_open_missions_by_agent(agent_id)
        if open_missions >= 3:
            raise HTTPException(status_code=400, detail= "already have 3 open missions")
        return mission_db.assign_mission(id, agent_id)
    
    except mission_utiles.MissionNotExists:
        raise HTTPException(status_code=404, detail= "The mission did not found")
    
    except agent_utiles.AgentNotFound:
        raise HTTPException(status_code=404, detail= "The agent did not found")

    except agent_utiles.AgentDoesNotActive:
        raise HTTPException(status_code=400, detail= "The agent not active")
    
    except mission_utiles.StatusNotNew:
        raise HTTPException(status_code=400, detail= "The status not new")
    
    except mission_utiles.NotCommander:
        raise HTTPException(status_code=400, detail= "The critical mision except just by commander")

    except connector.Error:
        raise HTTPException(status_code=500, detail=f"Something get wronng with the connection")
    
    except Exception:
        raise HTTPException(status_code=500, detail=f"Something get wronng.")
    
@router.put("/missions/{id}/start")
def start_mission(id:int):
    """docstring"""
    try:
        return mission_db.update_mission_status(id, "IN_PROGRESS")
    
    except mission_utiles.MissionNotExists:
        raise HTTPException(status_code=404, detail= "The mission did not found")
    
    except connector.Error:
        raise HTTPException(status_code=500, detail=f"Something get wronng with the connection")
    