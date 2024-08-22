import requests
from requests.auth import HTTPBasicAuth
import json
import csv

# Configuration for DHIS2 instance
dhis2_url = 'https://central.more-zm.org:8444'
username = 'chilando'
password = 'Kimye@%01'

# API endpoint for data values
data_values_endpoint = '/api/33/dataValueSets'

# Function to fetch data values
def get_data_values(dhis2_url, username, password, org_unit, period):
    params = {
        'orgUnit': org_unit,
        'period': period
    }
    url = f'{dhis2_url}{data_values_endpoint}'
    response = requests.get(url, auth=HTTPBasicAuth(username, password), params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch data values. Status code: {response.status_code}')
        print(response.text)
        return {}

# Function to transform data values
def transform_data_values(data_values):
    transformed = []
    for value in data_values['dataValues']:
        transformed.append({
            'dataid': value['dataElement'],
            'periodid': value['period'],
            'orguunitid': value['orgUnit'],
            'catecombo': value['categoryOptionCombo'],
            'attribute': value.get('attributeOptionCombo', ''),  # Attribute may not always be present
            'value': value['value']
        })
    return transformed

# Function to save data to JSON
def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Function to save data to CSV
def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Specify the organization unit and period
org_unit = 'your-orgunit-id'  # Replace with your actual org unit ID
period = '202301'             # Replace with your actual period ID

# Fetch data values from DHIS2
data_values = get_data_values(dhis2_url, username, password, org_unit, period)

# Transform data values
transformed_data = transform_data_values(data_values)

# Save transformed data to JSON and CSV
if transformed_data:
    save_to_json(transformed_data, 'data_values.json')
    save_to_csv(transformed_data, 'data_values.csv')
else:
    print('No data values to save')
