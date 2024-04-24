import mysql.connector
import os
import pandas as pd
from .dbconnect import DatabaseConnection
from ...TrainPipelines.Constant import Constant as cons
from .createdb import CreateDB


class UpdateDatabase:
    def __init__(self):
        pass

    def update(self,sentimentData):
        db=CreateDB(hostname="localhost",
                    database_name=cons.DATABASE_NAME,
                    username=cons.DATABASE_USERNAME,
                    password=cons.DATABASE_PASSWORD
                    )
        
        db.create()
        db.create_schema()
        source_connection = DatabaseConnection(hostname="localhost",
                                               database=cons.DATABASE_NAME,
                                               username=cons.DATABASE_USERNAME,
                                               password=cons.DATABASE_PASSWORD)

        # Retrieve healthscore values from source database
        FETCH = "SELECT AccountName, HealthScore FROM healthscore.customerhealthscore"
        source_data = source_connection.query(FETCH)

        healthscoreDF = self.convert(source_data)

        accountWiseHealth = self.calculateNewHealthScore(sentimentData,healthscoreDF)
        for index,row in healthscoreDF.iterrows():
            account_name = row['AccountName']
            healthscore  = accountWiseHealth[(accountWiseHealth['AccountName']==account_name)]['HealthScore'].values[0]

            try:
                source_connection.connect()
                update_query = "UPDATE CustomerHealthScore SET HealthScore = %s WHERE AccountName = %s"
                source_connection.query(update_query,row=(float(healthscore),account_name))
            finally:
                source_connection.disconnect()
        print("Table Updated!")




    def calculateNewHealthScore(self,sentiment,healthscoreData):

        '''Encoding : (positive: 0.5 , neutral: 0.0 , negative: -0.5)'''
        encoder_map = {"Positive":0.5,"Neutral":0.0,"Negative":-0.5}
        sentiment['encoded_sentiment'] = sentiment.sentiment.map(encoder_map)
        sentiment = sentiment.drop(['sentiment'],axis=1)

        '''Here  I am going to get the mean of all sentiment values'''
        grouped_data    = sentiment.groupby('Account').agg({
        'encoded_sentiment': 'mean',
        }).reset_index()


        maximum_threshold = 100
        minimum_threshold = -20

        temphealthscoreData = healthscoreData.copy()
        for index,row in temphealthscoreData.iterrows(): 
            adjusment = list(grouped_data[(grouped_data['Account']==row['AccountName'])]['encoded_sentiment'])
            if len(adjusment) == 0:
                temphealthscoreData.at[index,'HealthScore'] = row['HealthScore'] + 0
            else:
                temphealthscoreData.at[index,'HealthScore'] = row['HealthScore'] + adjusment[0]
        healthscoreData = temphealthscoreData
        

        # Apply thresholds
        healthscoreData['HealthScore'] = healthscoreData['HealthScore'].clip(lower=minimum_threshold, upper=maximum_threshold)

        return healthscoreData




    
    def convert(self,payload):
        data = payload
        df = pd.DataFrame(data, columns=['AccountName', 'HealthScore'])
        return df



