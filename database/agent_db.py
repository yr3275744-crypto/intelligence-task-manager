#TODO: add validation to size of the input value
# add validation function for create agent

from mysql import connector
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
        connection = None
        try:
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
            return row
        
        except agent_utiles.InvalidName as e:
            raise e
        
        except agent_utiles.InvalidSpecialty as e:
            raise e
        
        except agent_utiles.NoRank as e:
            raise e

        except agent_utiles.InvalidRank as e:
            raise e
        
        except connector.Error as e:
            raise e

        finally:
            if connection:
                connection.close()

    def get_all_agents(self) -> list:
        """docstring"""
        connection = None
        try:
            connection = DBConnection(database="Intelligence_db").get_connection()
            cursor = connection.cursor(dictionary = True)

            cursor.execute("SELECT * FROM agents")

            rows = cursor.fetchall()
            cursor.close()
            return rows
        
        finally:
            if connection:
                connection.close()

    def get_agent_by_id(self, id:int) -> dict | None:
        """docstring"""
        connection = None
        try:
            connection = DBConnection(database="Intelligence_db").get_connection()
            cursor = connection.cursor(dictionary = True)

            cursor.execute("SELECT * FROM agents WHERE id = %s", (id,))
            row = cursor.fetchone()
            
            cursor.close()
            return row if row else None
        
        finally:
            if connection:
                connection.close()

    def update_agent(self, id:int, data_dict:dict, cursor) -> bool:
        """docstring"""
        key_set_string = ", ".join([key + " = %s" for key in data_dict])
        values_and_id_list = list(data_dict.values()) + [id]
        update_strig = "UPDATE agents SET " + key_set_string + " WHERE id = %s"
        
        cursor.execute(update_strig, values_and_id_list)
        
        return True

    def update_agent_handle(self, id:int, data:AgentBody) -> str:
        """docstring"""
        connection = None
        try:
            if data.agent_rank:
                agent_utiles.check_is_valid_rank(data)
            
            connection = DBConnection(database="Intelligence_db").get_connection()
            cursor = connection.cursor(dictionary = True)

            data_dict = data.model_dump(exclude_none = True)
            if not data_dict:
                raise agent_utiles.EmptyInput

            is_exists = agent_utiles.check_if_exists(id, cursor)
            if not is_exists:
                return False    
            
            self.update_agent(id, data_dict, cursor)
            connection.commit()
            cursor.close()
            return True
            
        except agent_utiles.InvalidRank as e:
            raise e
        
        finally:
            if connection:
                connection.close()

    def deactivate_agent(self, id:int) -> str:
        """docstring"""
        connection = None
        try:
            connection = DBConnection(database="Intelligence_db").get_connection()
            cursor = connection.cursor(dictionary = True)

            is_exists = agent_utiles.check_if_exists(id, cursor)
            if not is_exists:
                raise agent_utiles.AgentNotFound

            cursor.execute("""UPDATE agents 
                        SET is_active = FALSE 
                        WHERE id = %s""", (id,))
            
            connection.commit()

            cursor.close()
            return f"The agent {id} deactivated successfully"
        
        finally:
            if connection:
                connection.close()

    def increment_completed(self, id:int) -> str:
        """docstring"""
        connection = DBConnection(database="Intelligence_db").get_connection()
        cursor = connection.cursor(dictionary = True)

        cursor.execute("""UPDATE agents 
                       SET completed_missions = completed_missions + 1 
                       WHERE id = %s""", (id,))

        connection.commit()
        changes_count = cursor.rowcount

        cursor.close()
        connection.close()

        if changes_count:
            return f"The agent {id} complite a task successfully"
        else:
            raise agent_utiles.AgentNotFound

    def increment_failed(self, id:int) -> str:
        """docstring"""
        connection = DBConnection(database="Intelligence_db").get_connection()
        cursor = connection.cursor(dictionary = True)

        cursor.execute("""UPDATE agents 
                       SET failed_missions = failed_missions + 1 
                       WHERE id = %s""", (id,))

        connection.commit()
        changes_count = cursor.rowcount

        cursor.close()
        connection.close()

        if changes_count:
            return f"The agent {id} faild to do a task."
        else:
            raise agent_utiles.AgentNotFound

    def get_agent_performance(self, id:int) -> dict:
        """docstring"""
        try:
            connection = DBConnection(database="Intelligence_db").get_connection()
            cursor = connection.cursor(dictionary = True)

            is_exists = agent_utiles.check_if_exists(id, cursor)
            if not is_exists:
                raise agent_utiles.AgentNotFound
            
            cursor.execute("""select completed_missions, failed_missions 
                        FROM agents
                        WHERE id = %s""", (id,))
            
            row = cursor.fetchone()

            row["total"] = row["completed_missions"] + row["failed_missions"]
            
            if row["total"] == 0:
                row["success_rate"] = 100
            else:
                row["success_rate"] = row["completed_missions"] / row["total"] *100

            return row
        
        finally:
            cursor.close()
            connection.close()

    # def agents_active_count(self) -> list:
    #     """docstring"""
    #     connection = DBConnection(database="Intelligence_db").get_connection()
    #     cursor = connection.cursor(dictionary = True)

    #     cursor.execute("SELECT COUNT(*) as active agents FROM agents WHERE is_active = TRUE")

    #     rows = cursor.fetchall()
    #     cursor.close()
    #     connection.close()
    #     return rows      


if __name__ == "__main__":
    agent_db = AgentDB()
    
    # an_agent = AgentBody(specialty = "fastapi all", agent_rank = "Senior")

    print(agent_db.increment_failed(6))
    # print(agent_db.create_agent(an_agent))

    # print(agent_db.get_all_agents())

    # print(agent_db.get_agent_by_id(1))

    # print(agent_db.update_agent_handle(1, an_agent))

    # print(agent_db.deactivate_agent(11))

    # print(agent_db.increment_completed(55))

    # print(agent_db.agents_active_count())