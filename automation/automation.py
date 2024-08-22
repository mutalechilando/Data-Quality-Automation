import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json

# Configuration for DHIS2 instances
source_dhis2_url = 'https://lpho.more-zm.org:8445/api/29'
target_dhis2_url = 'https://train.moh.gov.zm/lions/api/29/dataValueSets'
source_dhis2_username = 'mchilando'
source_dhis2_password = 'Chanda@10112020'
target_dhis2_username = 'admin'
target_dhis2_password = 'district'

# Parameters for data push
org_unit_id = 'ncgkwcQrfmc'  # Replace with your actual org unit ID - This is Kanyama First Level in MORE-ZM
period = '202302'  # Replace with your actual period (e.g., '202301' for January 2023)
dataset_id = 'N5mFDIePHXA'  # Replace with your actual dataset ID

# Function to load mappings from Excel file
def load_mappings(file_path, sheet_name=None, source_col='Original', target_col='Mapped'):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df.set_index(source_col)[target_col].to_dict()

# Load mappings from file
data_element_mapping = load_mappings('mappings_v1.xlsx', sheet_name='HIA2_MOREZM', source_col='morezm_dataid', target_col='hia2_dataid')
category_option_combo_mapping = load_mappings('mappings_v1.xlsx', sheet_name='HIA2_MOREZM', source_col='morezm_categoryoptioncomboid', target_col='hia2_categoryoptioncomboid')
org_unit_mapping = load_mappings('mappings_v1.xlsx', sheet_name='org_units', source_col='MORE-ZM', target_col='HIA2')

# Function to fetch data from DHIS2
def fetch_from_dhis2(url, username, password):
    response = requests.get(url, auth=HTTPBasicAuth(username, password), headers={'Accept': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch data from {url}. Status code: {response.status_code}')
        print(response.text)
        return {}

# Fetch data values from source DHIS2 (filtered by data element)
data_values_url = f'{source_dhis2_url}/dataValueSets?orgUnit={org_unit_id}&period={period}&dataSet={dataset_id}&paging=false'
data_values_data = fetch_from_dhis2(data_values_url, source_dhis2_username, source_dhis2_password)

# Transform data values to target DHIS2
transformed_data_values = []
for value in data_values_data.get('dataValues', []):
    transformed_value = {
        'dataElement': data_element_mapping.get(value['dataElement'], 'unknown_dataelement'),
        'period': value['period'],
        'orgUnit': org_unit_mapping.get(value['orgUnit'], 'unknown_orgunit'),
        'categoryOptionCombo': category_option_combo_mapping.get(value['categoryOptionCombo'], 'unknown_categorycombo'),
        #'attributeOptionCombo': category_option_combo_mapping.get(value.get('attributeOptionCombo', ''), 'unknown_attribute'),
        'value': value['value']
    }
    
    transformed_data_values.append(transformed_value)

payload = {
    "dataValues": transformed_data_values
}

filename = 'transformed_data_values_vv.json'

with open(filename, 'w') as json_file:
    json.dump(payload, json_file, indent=2)

print(f'Successfully stored transformed data to {filename}')

json_payload = json.dumps(payload)

# Set headers for JSON content
headers = {'Content-Type': 'application/json'}

# Authenticate with username and password
#auth = HTTPBasicAuth(username, password)

# Send the POST request
response = requests.post(target_dhis2_url, auth=HTTPBasicAuth(target_dhis2_username, target_dhis2_password), headers=headers, data=json_payload)

# Print the response
print(response.status_code)
print(response.json())