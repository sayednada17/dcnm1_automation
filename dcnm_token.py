import requests
import urllib3
import json
import getpass


DCNM_IP = input("Enter DCNM IP Address: ")
api_base_path = "https://"+DCNM_IP+"/rest/"

username = input("DCNM ADMIN USERNAME: ")
password = getpass.getpass("DCNM ADMIN PASSWORD: ")




def get_dcnm_token():
    try:
        urllib3.disable_warnings()
        header = {"Content-Type": "application/json"}
        payload = {"expirationTime": 1000000}
        hyperlink = api_base_path + "logon"
        response = requests.post(hyperlink, data=json.dumps(payload), verify=False, headers=header, auth=(username, password))
        if response.status_code == 200:
            print('logged into DCNM')
            dcnm_token = json.loads(response.content)['Dcnm-Token']
            return dcnm_token
    except Exception as e:
        return print("############## Error logging into DCNM.  Check credentials and try again", e)


