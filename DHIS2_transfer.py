import requests
from requests.auth import HTTPBasicAuth
import json

# Configuration for source DHIS2 instance
source_dhis2_url = 'https://source-dhis2-instance.org'
source_username = 'source-username'
source_password = 'source-password'

# Configuration for target DHIS2 instance
target_dhis2_url = 'https://target-dhis2-instance.org'
target_username = 'target-username'
target_password = 'target-password'

# API endpoints
data_elements_endpoint = '/api/dataElements'
org_units_endpoint = '/api/organisationUnits'

def get_data_elements(dhis2_url, username, password):
    url = f'{dhis2_url}{data_elements_endpoint}'
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    
    if response.status_code == 200:
        return response.json()['dataElements']
    else:
        print(f'Failed to fetch data elements. Status code: {response.status_code}')
        print(response.text)
        return []

def get_org_units(dhis2_url, username, password):
    url = f'{dhis2_url}{org_units_endpoint}'
    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    
    if response.status_code == 200:
        return response.json()['organisationUnits']
    else:
        print(f'Failed to fetch organisation units. Status code: {response.status_code}')
        print(response.text)
        return []

def push_data_element(dhis2_url, username, password, data_element):
    url = f'{dhis2_url}{data_elements_endpoint}'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers, data=json.dumps(data_element))
    
    if response.status_code in [200, 201]:
        print(f'Successfully pushed data element {data_element["id"]}')
    else:
        print(f'Failed to push data element {data_element["id"]}. Status code: {response.status_code}')
        print(response.text)

# Fetch data elements from source DHIS2
data_elements = get_data_elements(source_dhis2_url, source_username, source_password)

# Fetch organisation units from target DHIS2 (if needed for transformation)
org_units = get_org_units(target_dhis2_url, target_username, target_password)

# Push data elements to target DHIS2
for element in data_elements:
    # Transform data element if necessary, e.g., mapping organisation units
    # Example transformation: If you need to map org unit IDs, you would do it here
    # element['organisationUnits'] = [map_org_unit_id(org_unit) for org_unit in element['organisationUnits']]
    
    push_data_element(target_dhis2_url, target_username, target_password, element)

print('Data transfer complete.')
