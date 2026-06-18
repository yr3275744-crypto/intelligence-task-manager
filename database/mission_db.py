from mysql import connector
from database.db_connection import DBConnection
import mission_utiles
from mission_utiles import MissionCreateBody, MissionUpdateBody

class MissionDB:
    """docsrting"""
    def __init__(self):
        pass

    def create_mission(self, data:MissionCreateBody) -> dict:
        """docstring"""
        connection = None
        try:
            mission_utiles.check_difficulty_and_importance(data)

            risk_number = data.difficulty * 2 + data.importance
            if risk_number <= 9:
                risk_level = "LOW"
            elif risk_number <= 17:
                risk_level = "MEDIUM"
            elif risk_number <= 24:
                risk_level = "HIGH"
            elif risk_number >= 25:
                risk_level = "CRITICAL"

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