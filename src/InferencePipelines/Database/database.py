from .dbconnect import DatabaseConnection
from ...TrainPipelines.Constant import Constant as cons
from .createdb import CreateDB


'''Here what I am doing is creating , inserting, updating, deleting of database records.'''
class Database:
    def __init__(self,df):
        self.df = df
    
    def insertdb(self):
        db=CreateDB(hostname="localhost",
            database_name=cons.DATABASE_NAME,
            username=cons.DATABASE_USERNAME,
            password=cons.DATABASE_PASSWORD
            )
        
        db.create()
        db.create_schema()
        self.delete_all()
        source_connection = DatabaseConnection(hostname="localhost",
                                               database=cons.DATABASE_NAME,
                                               username=cons.DATABASE_USERNAME,
                                               password=cons.DATABASE_PASSWORD)

        # Retrieve healthscore values from source database
        for index, row in self.df.iterrows():
            INSERT = """INSERT INTO customerhealthscore (AccountName, HealthScore) VALUES (%s, %s)"""
            source_data = source_connection.query(INSERT,row=tuple(row))
    

    def delete_all(self):
        db=DatabaseConnection(hostname="localhost",
                              database=cons.DATABASE_NAME,
                              username=cons.DATABASE_USERNAME,
                              password=cons.DATABASE_PASSWORD
                              )
        db.connect()
        try:
            DELETE = "DELETE FROM customerhealthscore"
            db.query(DELETE)
        finally:
            db.disconnect()
