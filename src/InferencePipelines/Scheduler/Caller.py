import requests
import pandas as pd

from ..Database.updatedb import UpdateDatabase

class Caller:
    def __init__(self,api_endpoint,params):
        self.api_endpoint = api_endpoint
        self.params = params

    def convert_to_df(self,payload):
        lists = []
        if len(payload)  == 0:
            df = pd.DataFrame(columns=['Account','sentiment'])
        else:
            for lis in payload:
                lists.append(lis[::len(lis)-1])
            df = pd.DataFrame(data=lists,columns=['Account','sentiment'])
        return df


    def getPayload(self):
        try:
            response = requests.get(self.api_endpoint,params=self.params)
            response.raise_for_status()  
            sentimentPayload = response.json()
            return sentimentPayload
        except requests.exceptions.RequestException as e:
            print("Error fetching data:", e)
            return None
    
    def update(self):
        payload = self.getPayload()
        df = self.convert_to_df(payload)
        if len(payload) == 0:
            print("There are no updates!")
            pass
        else:
            updatedb = UpdateDatabase()
            updatedb.update(df)