#TODO: add validation to size of the input value

from db_connection import DBConnection
from pydantic import BaseModel
import pydantic

class AgentBody(BaseModel):
    name: str | None = None
    specialty: str | None = None
    agent_rank:str | None = None
    

class AgentDB:
    """Nust get name, specialty and agent_rank in the body.
    this check dun in another class or function"""
    def __init__(self):
        pass

    def create_agent(self, data:AgentBody) -> dict:
        """docstring"""

        values_tuple = (data.name, data.specialty, data.agent_rank)
        connection = DBConnection(database="Intelligence_db").get_connection()
        cursor = connection.cursor(dictionary = True)

        cursor.execute("INSERT INTO agents (name, specialty, agent_rank) VALUES (%s, %s, %s)", values_tuple)
        connection.commit()
        id = cursor.lastrowid
        cursor.execute("SELECT * FROM agents WHERE id = %s", (id,))
        row = cursor.fetchone()

        cursor.close()
        connection.close()
        return row



if __name__ == "__main__":
    agent_db = AgentDB()
    
    an_agent = AgentBody(name = "bob", specialty = "yoga", agent_rank = "Senior")

    print(agent_db.create_agent(an_agent))