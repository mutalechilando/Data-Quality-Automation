import requests
from requests.auth import HTTPBasicAuth
import json
import csv

# Configuration for DHIS2 instance
dhis2_url = 'https://lpho.more-zm.org:8445/api/' #https://lpho.more-zm.org:8445/api/29/organisationUnits/H0sIhCir6yk
username = 'mchilando'
password = 'Chanda@10112020'

# Parameters for data values
org_unit = 'H0sIhCir6yk'  #'ncgkwcQrfmc'  # Replace with your actual org unit ID
period = '202301'  # Replace with your actual period (e.g., '202301' for January 2023)
dataset_id = 'N5mFDIePHXA'  # Replace with your actual dataset ID

# API endpoint for data values
data_values_endpoint = '/dataValueSets'

# Function to fetch data values
def get_data_values(dhis2_url, username, password, org_unit, period, dataset_id):
    params = {
        'orgUnit': org_unit,
        'period': period,
        'dataSet': dataset_id,
        'paging': 'false'  # Add this to avoid pagination
    }
    url = f'{dhis2_url}{data_values_endpoint}'
    response = requests.get(url, auth=HTTPBasicAuth(username, password), params=params, headers={'Accept': 'application/json'})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch data values. Status code: {response.status_code}')
        print(response.text)
        return {}

# Function to save data values to JSON
def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Function to save data values to CSV
def save_to_csv(data_values, filename):
    keys = ['dataElement', 'period', 'orgUnit', 'categoryOptionCombo', 'attributeOptionCombo', 'value']
    with open(filename, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        for value in data_values['dataValues']:
            dict_writer.writerow({
                'dataElement': value['dataElement'],
                'period': value['period'],
                'orgUnit': value['orgUnit'],
                'categoryOptionCombo': value['categoryOptionCombo'],
                'attributeOptionCombo': value.get('attributeOptionCombo', ''),  # Attribute may not always be present
                'value': value['value']
            })

# Fetch data values from DHIS2
data_values = get_data_values(dhis2_url, username, password, org_unit, period, dataset_id)

# Save data values to JSON and CSV
if data_values:
    save_to_json(data_values, 'data_values.json')
    save_to_csv(data_values, 'data_values.csv')
    print('Data values saved to data_values.json and data_values.csv')
else:
    print('No data values to save')
