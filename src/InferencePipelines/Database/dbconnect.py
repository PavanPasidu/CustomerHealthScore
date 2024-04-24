import mysql.connector

from ...TrainPipelines.Constant import Constant

class DatabaseConnection:
    hostname = None
    database = None
    username = None
    password = None
    connection = None
    cursor = None
    query = None

    def __init__(self, hostname, database, username, password):
        if not self.connection:
            self.hostname = hostname
            self.database = database
            self.username = username
            self.password = password
            self.connect()

    def connect(self):
        ''' Connect the database
        '''
        self.connection = mysql.connector.connect(
            host     = self.hostname,
            user     = self.username,
            password = self.password,
            database = self.database
            )
        return self.connection

    def disconnect(self):
        '''Diconnect the database
        '''
        self.cursor.close()
        self.connection.close()
    
    def query(self, query,row=None):
        ''' Query the database.
            Return the list consist of quary output.
        ''' 
        result = []

        self.cursor = self.connection.cursor()
        self.cursor.execute(query,row)

        # Check if the query is INSERT, UPDATE, or DELETE
        if query.strip().lower().startswith(('insert', 'update', 'delete')):
            self.connection.commit()
            result = self.cursor.rowcount  
        else:
            for row in self.cursor:
                result.append(row)
        return result


    def count(self, table, condition = None):
        return len(self.simple_query(table, '*', condition))
  

    def deleteTable(self):
        global var3