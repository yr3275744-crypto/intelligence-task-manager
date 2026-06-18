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