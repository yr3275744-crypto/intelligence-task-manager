from fastapi import APIRouter, HTTPException
from mysql import connector
import database.mission_db
import database.agent_db
import mission_utiles

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