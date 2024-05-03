from fastapi import FastAPI, HTTPException, BackgroundTasks
import requests
import os
import json

from ..Constant import Constant as cons
from .Auth import Auth



class GetServicenowData(Auth):
    def __init__(self,url,const):
        super().__init__(url,const)
        self.url = url
           

    '''Get payload from servicenow'''
    def getJSONpayload(self,url,const):
        headers   = {'Content-Type': 'application/x-www-form-urlencoded'}
        FILE_PATH = './Tokens/accessTokens.json'

        # Get the access token
        with open(FILE_PATH,'w+') as js:
            try:
                CREDENTIALS = json.load(js)
            except json.decoder.JSONDecodeError as je:
                pass
        empty = (os.stat(FILE_PATH).st_size == 0)
        if empty:
            accessToken = super().getAccessToken(const=const)
        else:
            accessToken = CREDENTIALS.get('ACCESS_TOKEN')


        headers = {
            'Authorization': f'Bearer {accessToken}',
            'Content-Type': 'application/json'
        }

        params = {
            'startDate':'2022-02-01',
            'endDate':'2022-08-01'
        }
        response = requests.get(url, headers=headers, params=params)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            json_payload = response.json()
        else:
            print(f"Failed to retrieve data: {response.status_code} - {response.text}")
        return json_payload
    

