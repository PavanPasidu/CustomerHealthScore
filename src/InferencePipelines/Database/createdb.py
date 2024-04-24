from .dbconnect import DatabaseConnection

class CreateDB():
    def __init__(self, hostname, database_name, username, password):
        self.database_name=database_name
        self.hostname=hostname
        self.username=username
        self.password=password

    def create(self):
        databaseConnection = DatabaseConnection(self.hostname,None, self.username, self.password)
        databaseConnection.connect()
        databaseConnection.query("CREATE DATABASE IF NOT EXISTS {}".format(self.database_name))
        databaseConnection.disconnect
    def create_schema(self):
        healthscoreTable = """
            CREATE TABLE IF NOT EXISTS CustomerHealthScore (
            AccountName VARCHAR(255),
            HealthScore FLOAT
            );
        """

        databaseConnection2 = DatabaseConnection(self.hostname,self.database_name, self.username, self.password)
        databaseConnection2.connect()

        databaseConnection2.query(healthscoreTable)
        databaseConnection2.disconnect()
