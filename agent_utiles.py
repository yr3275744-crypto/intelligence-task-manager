from pydantic import BaseModel

VALID_AGENT_RANK = ("Junior", "Senior", "Commander")

class InvalidName(Exception):
    pass

class InvalidSpecialty(Exception):
    pass

class NoRank(Exception):
    pass

class InvalidRank(Exception):
    pass

class EmptyInput(Exception):
    pass

class AgentNotFound(Exception):
    pass

class AgentDoesNotActive(Exception):
    pass


class AgentBody(BaseModel):
    name: str | None = None
    specialty: str | None = None
    agent_rank:str | None = None
    

def check_full_detiles(body:AgentBody):
    """docstring"""
    if not body.name:
        raise InvalidName
    if not body.specialty:
        raise InvalidSpecialty
    if not body.agent_rank:
        raise NoRank
    
def check_is_valid_rank(body:AgentBody):
    """docstring"""
    if body.agent_rank not in VALID_AGENT_RANK:
        raise InvalidRank
    
def check_if_exists(id:int, cursor):
    """docstring"""
    cursor.execute("SELECT * FROM agents WHERE id = %s", (id,))
    row = cursor.fetchone()
    return row if row else None