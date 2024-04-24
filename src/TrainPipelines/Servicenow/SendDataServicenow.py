import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin

class PutDataServicenow:
    def push_dataframe_to_servicenow(df, table_name, instance_url, username, password):
        """
        Pushes data from a DataFrame to a ServiceNow table.
        
        Args:
            df (pandas.DataFrame): DataFrame containing the data to push.
            table_name (str): Name of the ServiceNow table.
            instance_url (str): URL of the ServiceNow instance.
            username (str): Username for authentication.
            password (str): Password for authentication.
            
        Returns:
            bool: True if data is successfully pushed, False otherwise.
        """
        try:
            # Convert DataFrame to JSON
            json_data = df.to_json(orient='records')

            # Construct the API endpoint
            api_endpoint = urljoin(instance_url, f'/api/now/table/{table_name}')

            # Construct headers for authentication
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            # Send data to ServiceNow
            response = requests.post(api_endpoint, auth=HTTPBasicAuth(username, password), headers=headers, data=json_data)

            # Handle response
            if response.status_code == 200:
                print("Data successfully pushed to ServiceNow")
                return True
            else:
                print("Error:", response.text)
                return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    if __name__ == "__main__":
        #  DataFrame
        data = {
            'name': '',
           
        }
        df = pd.DataFrame(data)

        # ServiceNow instance details
        instance_url = 'https://'
        username = ''
        password = ''
        table_name = ''

        # Push DataFrame to ServiceNow
        push_success = push_dataframe_to_servicenow(df, table_name, instance_url, username, password)
        if push_success:
            print("Data successfully pushed to ServiceNow")
        else:
            print("Failed to push data to ServiceNow")



import pandas as pd
import requests

#  DataFrame
data = {
    'name': '',
    
}
df = pd.DataFrame(data)

# OAuth 2.0 authentication details
client_id = ''
client_secret = ''
username = ''
password = ''
oauth_url = 'https://your_instance/oauth_token.do'
instance_url = 'https://your_instance/api/now/table/your_table_name'

# Authenticate with ServiceNow using OAuth 2.0
oauth_data = {
    'grant_type': 'password',
    'client_id': client_id,
    'client_secret': client_secret,
    'username': username,
    'password': password
}
oauth_response = requests.post(oauth_url, data=oauth_data)
access_token = oauth_response.json()['access_token']

# Construct headers with OAuth 2.0 access token
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer ' + access_token
}

# Convert DataFrame to JSON
json_data = df.to_json(orient='records')

# Construct the API endpoint
api_endpoint = instance_url

# Send data to ServiceNow
response = requests.post(api_endpoint, headers=headers, data=json_data)

# Handle response
if response.status_code == 200:
    print("Data successfully pushed to ServiceNow")
else:
    print("Error:", response.text)
