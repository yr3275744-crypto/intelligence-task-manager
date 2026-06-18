from pydantic import BaseModel
import agent_utiles
VALID_STATUS = ("NEW", "ASSIGNED", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED")

class MissionCreateBody(BaseModel):
    title: str
    description: str
    location: str
    difficulty: int
    importance: int

class MissionUpdateBody(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    difficulty: int
    importance: int


class InvalidDifficultyOrImportance(Exception):
    pass

# class InvalidImportance(Exception):
#     pass

class MissionNotExists(Exception):
    pass

class StatusNotNew(Exception):
    pass

class NotCommander(Exception):
    pass

def check_difficulty_and_importance(body:MissionCreateBody) -> bool:
    """docstring"""
    if body.difficulty >= 1 and body.difficulty <= 10:
        valid = True
    else:
        raise InvalidDifficultyOrImportance
    
    if body.importance >= 1 and body.importance <= 10:
        valid = True
    else:
        raise InvalidDifficultyOrImportance
    
    return valid
    
def get_mission_if_exists_else_None(id:int, cursor):
    """docstring"""
    cursor.execute("SELECT * FROM missions WHERE id = %s", (id,))
    row = cursor.fetchone()
    return row if row else None

def check_for_assign(mission_id:int, agent_id:int, cursor) -> bool:
    """docstring"""
    agent = agent_utiles.check_if_exists(agent_id, cursor)
    if not agent:
        raise agent_utiles.AgentNotFound
    
    if not agent.get("is_active"):
        raise agent_utiles.AgentDoesNotActive
    
    mission = get_mission_if_exists_else_None(mission_id, cursor)
    if not mission:
        raise MissionNotExists
    
    if mission.get("status") != "NEW":
        raise StatusNotNew
    
    if mission.get("risk_level") == "CRITICAL" and agent.get("agent_rank") != "Commander":
        raise NotCommander