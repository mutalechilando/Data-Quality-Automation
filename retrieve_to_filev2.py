import requests
from requests.auth import HTTPBasicAuth
import json
import csv
import os

# Configuration for DHIS2 instance
dhis2_url = 'https://lpho.more-zm.org:8445/api/29'
username = 'mchilando'
password = 'Chanda@10112020'

# Parameters for data values
org_unit_id = 'ncgkwcQrfmc'  # Replace with your actual org unit ID
period = '202401'  # Replace with your actual period (e.g., '202301' for January 2023)
dataset_id = 'N5mFDIePHXA'  # Replace with your actual dataset ID

# Function to fetch data from DHIS2
def fetch_from_dhis2(url, username, password):
    response = requests.get(url, auth=HTTPBasicAuth(username, password), headers={'Accept': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch data from {url}. Status code: {response.status_code}')
        print(response.text)
        return {}

# Fetch organization unit name
org_unit_url = f'{dhis2_url}/organisationUnits/{org_unit_id}'
org_unit_data = fetch_from_dhis2(org_unit_url, username, password)
org_unit_name = org_unit_data.get('displayName', 'unknown_orgunit')

# Fetch data elements
data_elements_url = f'{dhis2_url}/dataElements'
data_elements_data = fetch_from_dhis2(data_elements_url, username, password)
data_elements = {de['id']: de['displayName'] for de in data_elements_data.get('dataElements', [])}

# Fetch category option combos
category_combos_url = f'{dhis2_url}/categoryOptionCombos'
category_combos_data = fetch_from_dhis2(category_combos_url, username, password)
category_combos = {cc['id']: cc['displayName'] for cc in category_combos_data.get('categoryOptionCombos', [])}

# Fetch data values
data_values_url = f'{dhis2_url}/dataValueSets?orgUnit={org_unit_id}&period={period}&dataSet={dataset_id}&paging=false'
data_values_data = fetch_from_dhis2(data_values_url, username, password)

# Prepare data for output
transformed_data = []
for value in data_values_data.get('dataValues', []):
    transformed_data.append({
        'dataElement': value['dataElement'],
        'period': value['period'],
        'orgUnit': value['orgUnit'],
        'categoryOptionCombo': value['categoryOptionCombo'],
        'attributeOptionCombo': value['attributeOptionCombo'],
        'value': value['value']
    })

# File names with orgunit name and period
json_filename = f'data_values_{org_unit_name}_{period}.json'
csv_filename = f'data_values_{org_unit_name}_{period}.csv'

# Ensure file names are filesystem-safe
#json_filename = "".join([c if c.isalnum() else "_" for c in json_filename])
#csv_filename = "".join([c if c.isalnum() else "_" for c in csv_filename])

# Save data to JSON
with open(json_filename, 'w') as f:
    json.dump(transformed_data, f, indent=2)
print(f'Data values saved to {json_filename}')

# Save data to CSV
keys = ['dataElement', 'period', 'orgUnit', 'categoryOptionCombo', 'attributeOptionCombo', 'value']
with open(csv_filename, 'w', newline='') as f:
    dict_writer = csv.DictWriter(f, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(transformed_data)
print(f'Data values saved to {csv_filename}')
