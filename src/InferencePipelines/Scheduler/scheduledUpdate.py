'''Here I will call the sentiment API to get sentiment Account wise.
   And accordingly healthscore will be updated. (Sentiment values will come as batches)
'''

from datetime import date,timedelta
from fastapi import FastAPI,BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler as scheduler
import requests
import pandas as pd
from .Caller import Caller

from ..Database.updatedb import UpdateDatabase


class Scheduler:
    def __init__(self):
        self.df =  pd.DataFrame()
        self.sentimentPayload  =  None
        self.start = date.today() - timedelta(days=1)
        self.end = date.today() - timedelta(days=1)


    def scheduleUpdate(self):
        params       = {
            'start':self.start,
            'end':self.end,
        }
        api_endpoint = "http://127.0.0.1:8000/get_comments"


        sch = scheduler()
        caller = Caller(api_endpoint=api_endpoint,params=params)
        sch.add_job(caller.update,trigger='cron',hour=10,  minute=38)
        sch.start()

        try:
            print('Scheduler started, ctrl+c to exit!')
            while 1:
                pass
        except KeyboardInterrupt:
            if sch.state:
                sch.shutdown()
        sch.add_job(func=caller.update)



# class Updater(Scheduler):
#     def __init__(self):
#         super().__init__()

#     def updateHealthscore(self,status,df):
#         if status == 'success':
#             UpdateDatabase.update(df)
#         else:
#             print("Unexpected error occured!!!")


#     def convertData(self,dataJson):
#         dataField = dataJson['result']['data']
#         status =  dataJson['result']['status']
#         header_fields = dataField[0].keys()
#         rows = dataField

#         self.df = pd.DataFrame(rows, columns=header_fields)
#         return self.df,status


#     def get_json_payload(self,api_endpoint,params):
#         global df
#         try:
#             response = requests.get(api_endpoint,params=params)
#             response.raise_for_status()  
#             sentimentPayload = response.json()

#             if sentimentPayload.has_key('result'):
#                 df,status = self.convertData(sentimentPayload) 
#                 self.updateHealthscore(status=status,df=df)
#             elif sentimentPayload.has_key('error'):
#                 print("Error has occured while fetching data.")

#         except requests.exceptions.RequestException as e:
#             print("Error fetching data:", e)
#             return None
        







