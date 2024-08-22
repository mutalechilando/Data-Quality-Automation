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

# Parameters for data push
org_unit_id = 'ncgkwcQrfmc'  # Replace with your actual org unit ID - This is Kanyama First Level in MORE-ZM
period = '202301'  # Replace with your actual period (e.g., '202301' for January 2023)
dataset_id = 'N5mFDIePHXA'  # Replace with your actual dataset ID
specific_data_element_id = 'IaN588shABx'  # Replace with the ID of the specific data element - MORE-ZM -> TX_CURR_N: Number of adults and children receiving ART

# Mappings for IDs (update as needed)
data_element_mapping = {
    specific_data_element_id: 'xC1fdx2189O',  # Map the specific data element ID -> Currently on ART in HIA2
    # Add other mappings if necessary
}

category_option_combo_mapping = {
    'Qmd2frB3e8F':'Etb79cTNmIK',
    'nMsMRcdsXmy':'ZjHIkuvbhVC',
    'RQXs6B8Td4v':'GJ9gSSmJoIv',
    'wcvVlUrzbYG':'rj1w1Pq8jkf',
    'N78akNFqLex':'C56tlhPFjfp',
    'onwJ6bulsyi':'VZ2XN0ZxA6S',
    'RT7QsVY15yL':'P02eYTPt4dS',
    'pUXn4laGtJe':'uIpRFk3Jgz6',
    'udSjk1sKgO5':'y01Z8E2MBYt',
    'FZZZIfer5tA':'Y4YXc8CkgNT',
    'g10r90Dfqno':'KaUFNUYC7ft',
    'TT9hQ7SaHea':'WqDPWzWmlQT',
    'dwskguR0DV8':'fzKC3XrqoHz',
    'BqGKadWCFhx':'Ak2FdPn5Q9G',
    'subJjGY0UcE':'puTb3F0KdEX',
    'tpKwyj8il3w':'Qqla7AHVmyE',
    'Il7UBf5AxcH':'u3zNA6CU0aC',
    'Mwqc3GO1kId':'CTYuhOgISwV',
    'SmLUO99wdfb':'oT9hPGqZ3pC',
    'IzV4BuohS90':'zqBB8YN5eze',
    'EMovAqLcbGq':'zqBB8YN5eze',
    'GnlieRaxUWw':'zqBB8YN5eze',
    'Yt9tkigTSBr':'u3zNA6CU0aC',
    'W909S6WDrZ8':'u3zNA6CU0aC',
    'Il7UBf5AxcH':'u3zNA6CU0aC',
    'ETwXuMGk1iE':'u3zNA6CU0aC',
    'TSt8KAsSu0I':'u3zNA6CU0aC',

    # Add mappings for desired category option combos here
}

org_unit_mapping = {
    org_unit_id: 'ou0987654321',  # Map the specific org unit ID -> Get Kanyama First Level from HIA2
    # Add other mappings if necessary
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

# Fetch data values from source DHIS2 (filtered by data element)
data_values_url = f'{source_dhis2_url}/dataValueSets?orgUnit={org_unit_id}&period={period}&dataSet={dataset_id}&filter=dataElement:{specific_data_element_id}&paging=false'
data_values_data = fetch_from_dhis2(data_values_url, source_dhis2_username, source_dhis2_password)

    # Filter for desired category option combo IDs
desired_category_combo_ids = []  # Replace with your desired IDs


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
    
    #if transformed_value['categoryOptionCombo'] in desired_category_combo_ids:
    transformed_data_values.append(transformed_value)
 

# Prepare payload for target DHIS2
payload = {
    'dataSet': 'your_dataset_id',
    'completeDate': '2024-07-24' 
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

