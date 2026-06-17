#TODO: add validation to size of the input value
# add validation function for create agent

from database.db_connection import DBConnection
import agent_utiles
from agent_utiles import AgentBody

class AgentDB:
    """Nust get name, specialty and agent_rank in the body.
    this check dun in another class or function"""
    def __init__(self):
        pass

    def create_agent(self, data:AgentBody) -> dict:
        """docstring"""
        agent_utiles.check_full_detiles(data)
        agent_utiles.check_is_valid_rank(data)

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

    def get_all_agents(self) -> list:
        """docstring"""
        connection = DBConnection(database="Intelligence_db").get_connection()
        cursor = connection.cursor(dictionary = True)

        cursor.execute("SELECT * FROM agents")

        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows        

    def get_agent_by_id(self, id:int) -> dict | None:
        """docstring"""
        connection = DBConnection(database="Intelligence_db").get_connection()
        cursor = connection.cursor(dictionary = True)

        cursor.execute("SELECT * FROM agents WHERE id = %s", (id,))
        row = cursor.fetchone()
        
        cursor.close()
        connection.close()
        return row if row else None

    def update_agent(self, id:int, data:AgentBody) -> str:
        """docstring"""
        if data.agent_rank:
            agent_utiles.check_is_valid_rank(data)
        
        connection = DBConnection(database="Intelligence_db").get_connection()
        cursor = connection.cursor(dictionary = True)

        data_dict = data.model_dump(exclude_none = True)
        if not data_dict:
            raise agent_utiles.EmptyInput

        key_set_string = ", ".join([key + " = %s" for key in data_dict])
        values_and_id_list = list(data_dict.values()) + [id]
        update_strig = "UPDATE agents SET " + key_set_string + " WHERE id = %s"
        
        cursor.execute(update_strig, values_and_id_list)
        connection.commit()

        cursor.close()
        connection.close() 
        return f"The agent {id} is updated successfully"


if __name__ == "__main__":
    agent_db = AgentDB()
    
    an_agent = AgentBody(specialty = "oop", agent_rank = "Senior")

    # print(agent_db.create_agent(an_agent))

    # print(agent_db.get_all_agents())

    # print(agent_db.get_agent_by_id(1))

    # print(agent_db.update_agent(1, an_agent))