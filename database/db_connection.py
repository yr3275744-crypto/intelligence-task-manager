from mysql import connector

class DBConnection:
    """docstring"""
    def __init__(self, user:str = "root", password:str = "1234", port:str = "3306", database:str | None = None):
        self.user = user
        self.password = password
        self.port = port
        self.database = database
    
    def get_connection(self):
        """docstring"""
        try:
            if self.database:
                return connector.connect(
                    user = self.user,
                    password = self.password,
                    port = self.port,
                    database = self.database
                )
            else:
                return connector.connect(
                    user = self.user,
                    password = self.password,
                    port = self.port
                )
        
        except connector.Error as error:
            raise error
        

    def create_database(self) -> str:
        """docstring"""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")

        cursor.close()
        self.database = "Intelligence_db"
        return "The database is created successfuly or already exists"

    def create_tables(self) -> str:
        """docstring"""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS agents(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(50) NOT NULL,
                       specialty VARCHAR(50) NOT NULL,
                       is_active BOOLEAN DEFAULT TRUE,
                       completed_missions INT DEFAULT 0,
                       failed_missions INT DEFAULT 0,
                       agent_rank ENUM('Junior', 'Senior', 'Commander'))""")

        connection.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS missions(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       title VARCHAR(100) NOT NULL,
                       description TEXT NOT NULL,
                       location VARCHAR(100) NOT NULL,
                       difficulty INT NOT NULL,
                       importance INT NOT NULL,
                       status VARCHAR(50) DEFAULT 'NEW',
                       risk_level VARCHAR(50) NOT NULL,
                       assigned_agent_id INT DEFAULT NULL)""")
        connection.commit()

        cursor.close()
        connection.close()
        return "The tables are created successfully"


if __name__ == "__main__":
    db_connection = DBConnection()
    connection = db_connection.get_connection()
    print("success")
    connection.close()
    db_connection.create_database()
    db_connection.get_connection()
    connection.close()
    print(db_connection.create_tables())
    print(db_connection.database)