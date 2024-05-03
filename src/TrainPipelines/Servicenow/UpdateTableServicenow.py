import pandas as pd
import requests
import json
import os
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin

from ..Constant import Constant
from .Auth import Auth

class PutDataServicenow(Auth):
    def __init__(self, table_name, instance_url, auth_url):
        super().__init__(auth_url, Constant)
        self.table_name = table_name
        self.instance_url = instance_url
        
    def push_dataframe_to_servicenow(self, df, const):
        try:
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
            self.post(header=headers, df=df)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False


    def postRequest(self, headers, data):
        # Send data to ServiceNow
        response = requests.post(self.instance_url,  
                                headers = headers, 
                                data = data)
        if response.status_code == 201:
            print("Data successfully pushed to ServiceNow")
            return True
        else:
            print("Error:", response.text)
            return False

    def post(self, header, df):
        record_dict = {"records":[]}
        for index,row in df.iterrows():
            data = {
                "u_account_name": row['account_name'],
                "u_fcr_percentage": row['is_fcr'],
                "u_impact_of_products": row['encoded_product_impact'],
                "u_mean_agent_reassignment_count": row['agent_reassignment_count'],
                "u_mean_reopen_count": row['reopen_count'],
                "u_mean_time_to_resolve": row['time_to_resolve'],
                "u_sales_region": row['Sales Region'],
                "u_sub_region": row['Sub Region'],
                "u_survey": row['Survey Campaign'],
                "u_health_score": row['healthScore'],
            }
            json_payload = json.dumps(data)
            record_dict["records"].append(json_payload)
        json_payload_dict = json.dumps(record_dict)
        self.postRequest(headers=header, data=json_payload_dict)



class GetDataServicenow(Auth):
    def __init__(self, auth_url):
        super().__init__(auth_url, Constant)

    