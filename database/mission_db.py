from mysql import connector
from database.db_connection import DBConnection
import mission_utiles
from mission_utiles import MissionCreateBody, MissionUpdateBody

class MissionDB:
    """docsrting"""
    def __init__(self):
        pass

    def calculate_risk_level(self, risk_number:int) -> str:
        """docstring"""
        if risk_number <= 9:
            risk_level = "LOW"
        elif risk_number <= 17:
            risk_level = "MEDIUM"
        elif risk_number <= 24:
            risk_level = "HIGH"
        elif risk_number >= 25:
            risk_level = "CRITICAL"
        
        return risk_level


    def create_mission(self, data:MissionCreateBody) -> dict:
        """docstring"""
        connection = None
        try:
            mission_utiles.check_difficulty_and_importance(data)

            risk_number = data.difficulty * 2 + data.importance
            risk_level = self.calculate_risk_level(risk_number)

            values_tuple = (data.title, data.description, data.location, data.difficulty, data.importance, risk_level)
            connection = DBConnection(database="Intelligence_db").get_connection()
            cursor = connection.cursor(dictionary = True)

            cursor.execute("""INSERT INTO missions 
                           (title, description, location, difficulty, importance, risk_level) 
                           VALUES (%s, %s, %s, %s, %s, %s)""", values_tuple)
            connection.commit()
            id = cursor.lastrowid
            cursor.execute("SELECT * FROM missions WHERE id = %s", (id,))
            row = cursor.fetchone()
            cursor.close()
            return row
        
        except mission_utiles.InvalidDifficultyOrImportance as e:
            raise e
        
        except connector.Error as e:
            raise e
        
        finally:
            if connection:
                connection.close()

    def get_all_missions(self) -> list:
        """docstring"""
        connection = None
        try:
            connection = DBConnection(database="Intelligence_db").get_connection()
            cursor = connection.cursor(dictionary = True)

            cursor.execute("SELECT * FROM missions")

            rows = cursor.fetchall()
            cursor.close()
            return rows
        
        finally:
            if connection:
                connection.close()

    def get_mission_by_id(self, id:int) -> dict | None:
        """docstring"""
        connection = None
        try:
            connection = DBConnection(database="Intelligence_db").get_connection()
            cursor = connection.cursor(dictionary = True)

            cursor.execute("SELECT * FROM missions WHERE id = %s", (id,))
            row = cursor.fetchone()
            
            cursor.close()
            return row if row else None
        
        finally:
            if connection:
                connection.close()

    def assign_mission(self, m_id:int, a_id:int) -> str:
        """docstring"""
        connection = None
        try:
            connection = DBConnection(database="Intelligence_db").get_connection()
            cursor = connection.cursor(dictionary = True)
            mission_utiles.check_for_assign(m_id, a_id, cursor)

            cursor.execute("UPDATE missions SET assigned_agent_id = %s WHERE id = %s", (a_id, m_id))
            
            connection.commit()

            return "The mission assign was successful."
        
        finally:
            if connection:
                connection.close()

    def get_open_missions_by_agent(self, id:int):
        """docstring"""
        connection = None
        try:
            connection = DBConnection(database="Intelligence_db").get_connection()
            cursor = connection.cursor(dictionary = True)
            
            cursor.execute("""SELECT COUNT(*) as count
                           FROM missions 
                           WHERE (status = 'ASSIGNED' OR STATUS = 'IN_PROGRESS') AND assigned_agent_id = %s""", (id,))

            row = cursor.fetchone()
            cursor.close()

            return row["count"]
        
        finally:
            if connection:
                connection.close()


if __name__ == "__main__":
    m = MissionDB()
    print(m.get_open_missions_by_agent(3))