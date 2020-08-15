import requests
import json
import csv
from pprint import pprint

import dcnm_token as dt

dcnm_ip = dt.DCNM_IP
api_base_path = dt.api_base_path

token = dt.get_dcnm_token()


def main():
    json_input_switches = get_csv_switches()
    dcnm_fabrics = list_fabrics()
    poap_switch = poap_switches(json_input_switches,dcnm_fabrics)



def get_csv_switches():
    try:
        print('=======================Collecting Switches information from CSV file=====================')
        csv_sw_list = []
        csv_switches = open('switches.csv', 'r')
        switches = csv.DictReader(csv_switches, delimiter=',')

        for row in switches:
            csv_sw_list.append(row)
        json_switches = json.loads(json.dumps(csv_sw_list))
        # pprint(json_switches)
        return json_switches
    except Exception as e:
        return print('something went wrong')


def list_fabrics():
    try:
        payload = {}
        header = {'Content-Type': 'application/json', 'Dcnm-Token': token}
        hyperlink = api_base_path + 'control/fabrics'

        response = requests.get(hyperlink, data=json.dumps(payload), verify=False, headers=header)
        if response.status_code == 200:
            print('=======================Collecting Fabrics from DCNM=====================')
            fabrics = json.loads(response.content)
            print('=================== DCNM is Managing The Below Fabrics==================')
            print(([fabric['fabricName'] for fabric in fabrics]))
            return ([fabric['fabricName'] for fabric in fabrics])
        elif response.status_code == 401:
            return print('Unauthorized access to API, Check the USERNAME and PASSWORD')

    except Exception as e:
        print('=======================Collecting Fabrics from DCNM=====================')
        return print(response.status_code)



def poap_switches(json_input_switches,dcnm_fabrics):
    try:

        poap_fabric = input(f'Enter the fabric the switches should be poap into {dcnm_fabrics} :')
        password = dt.password
        discoveryUsername = dt.username
        discoveryPassword = dt.password

        print('The POAP process has started')

        for input_entry in json_input_switches:
            payload = {}
            header = {'Content-Type': 'application/json', 'Dcnm-Token': token}
            hyperlink = api_base_path + 'control/fabrics/' + poap_fabric + '/inventory/poap'
            switch_data = {"modulesModel": [str(input_entry["model"])],
                           "gateway": str(input_entry["gateway"])
                           }

            payload = {"serialNumber": str(input_entry["serialNumber"]),
                       "model": str(input_entry["model"]),
                       "version": str(input_entry["version"]),
                       "hostname": str(input_entry["hostname"]),
                       "ipAddress": str(input_entry["ipAddress"]),
                       "password": password,
                       "discoveryUsername": discoveryUsername,
                       "discoveryPassword": discoveryPassword,
                       "data": json.dumps(switch_data)
                       }

            print(payload['hostname'] + ':' + payload['ipAddress'] + ' has been POAP')

            response = requests.post(hyperlink, data=json.dumps([payload]), verify=False, headers=header)

        return print('========The POAP Process have been completed================')
    except Exception as e:
        return print('something went wrong', e)


if __name__ == "__main__":
    main()
