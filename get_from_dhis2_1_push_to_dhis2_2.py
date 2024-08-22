import requests
from requests.auth import HTTPBasicAuth
import json

# Configuration for DHIS2 instances
source_dhis2_url = 'https://lpho.more-zm.org:8445/api/29'
target_dhis2_url = 'https://target-dhis2-instance.org/api/29'
source_dhis2_username = 'your-username'
source_dhis2_password = 'your-password'
target_dhis2_username = 'your-username'
target_dhis2_password = 'your-password'

# Parameters for data values
org_unit_id = 'your-orgunit-id'  # Replace with your actual org unit ID
period = '202301'  # Replace with your actual period (e.g., '202301' for January 2023)
dataset_id = 'N5mFDIePHXA'  # Replace with your actual dataset ID

# Mappings for IDs
data_element_mapping = {
    'de1234567890': 'de0987654321',
    'de2345678901': 'de8765432109',
    'de3456789012': 'de7654321098',
    # Add all necessary mappings here
}

category_option_combo_mapping = {
    'coc1234567890': 'coc0987654321',
    'coc2345678901': 'coc8765432109',
    'coc3456789012': 'coc7654321098',
    # Add all necessary mappings here
}

org_unit_mapping = {
    'ou1234567890': 'ou0987654321',
    'ou2345678901': 'ou8765432109',
    'ou3456789012': 'ou7654321098',
    # Add all necessary mappings here
}

# Function to fetch data from DHIS2
def fetch_from_dhis2(url, username, password):
    response = requests.get(url, auth=HTTPBasicAuth(username, password), headers={'Accept': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch data from {url}. Status code: {response.status_code}')
        print(response.text)
        return {}

# Fetch data values from source DHIS2
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
        'attributeOptionCombo': category_option_combo_mapping.get(value.get('attributeOptionCombo', ''), 'unknown_attribute'),
        'value': value['value']
    }
    transformed_data_values.append(transformed_value)

# Prepare payload for target DHIS2
payload = {
    'dataValues': transformed_data_values
}

# Push data to target DHIS2
def push_to_dhis2(url, username, password, payload):
    response = requests.post(url, auth=HTTPBasicAuth(username, password), json=payload, headers={'Content-Type': 'application/json'})
    if response.status_code in [200, 201]:
        print(f'Successfully pushed data to {url}')
    else:
        print(f'Failed to push data to {url}. Status code: {response.status_code}')
        print(response.text)

target_data_values_url = f'{target_dhis2_url}/dataValueSets'
push_to_dhis2(target_data_values_url, target_dhis2_username, target_dhis2_password, payload)
