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
        

    def create_database(self) -> None:
        """docstring"""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")
        print("The database is created successfuly or already exists")
        cursor.close()
        self.database = "Intelligence_db"
        return None



if __name__ == "__main__":
    db_connection = DBConnection()
    connection = db_connection.get_connection()
    print("success")
    connection.close()
    db_connection.create_database()
    db_connection.get_connection()
    connection.close()