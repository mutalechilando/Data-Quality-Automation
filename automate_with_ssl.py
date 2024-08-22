import os
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to read credentials from a file
def read_credentials(file_path):
    credentials = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                credentials[key] = value
    except Exception as e:
        logging.error(f'Error reading credentials from {file_path}: {e}')
    return credentials
    

# Read credentials from the file
credentials_file = 'credentials.txt'
credentials = read_credentials(credentials_file)

# Configuration for DHIS2 instances
source_dhis2_url = os.getenv('SOURCE_DHIS2_URL', 'https://lpho.more-zm.org:8445/api/29')
target_dhis2_url = os.getenv('TARGET_DHIS2_URL', 'https://train.moh.gov.zm/lions/api/29/dataValueSets')
source_dhis2_username = credentials.get('SOURCE_DHIS2_USERNAME', 'admin')
source_dhis2_password = credentials.get('SOURCE_DHIS2_PASSWORD', 'district')
target_dhis2_username = credentials.get('TARGET_DHIS2_USERNAME', 'admin')
target_dhis2_password = credentials.get('TARGET_DHIS2_PASSWORD', 'district')

# Parameters for data push
org_unit_id = 'ncgkwcQrfmc'  # Replace with your actual org unit ID - This is Kanyama First Level in MORE-ZM
period = '202403'  # Replace with your actual period (e.g., '202301' for January 2023)
dataset_id = 'N5mFDIePHXA'  # Replace with your actual dataset ID

# Path to SSL certificate
cert_path = 'LPHO Certificate/lpho.more-zm.org.crt'  # Update this with the correct path to your SSL certificate

# Function to load mappings from Excel file
def load_mappings(file_path, sheet_name=None):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        logging.error(f'Error loading mappings: {e}')
        return pd.DataFrame()

# Load mappings from the Excel file
file_path = 'mappings_v1.xlsx'
mappings_df = load_mappings(file_path, sheet_name='HIA2_MOREZM')
org_unit_mapping = load_mappings(file_path, sheet_name='org_units').set_index('MORE-ZM')['HIA2'].to_dict()

# Function to fetch data from DHIS2
def fetch_from_dhis2(url, username, password, cert_path=None):
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password), headers={'Accept': 'application/json'}, verify=cert_path)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f'Failed to fetch data from {url}. Status code: {response.status_code}')
            logging.error(response.text)
            return {}
    except requests.exceptions.SSLError as e:
        logging.error(f'SSL Error: {e}')
        return {}
    except Exception as e:
        logging.error(f'Error fetching data from DHIS2: {e}')
        return {}
        
# Fetch data values from source DHIS2 (filtered by data element)
data_values_url = f'{source_dhis2_url}/dataValueSets?orgUnit={org_unit_id}&period={period}&dataSet={dataset_id}&paging=false'
data_values_data = fetch_from_dhis2(data_values_url, source_dhis2_username, source_dhis2_password, cert_path=cert_path)

if data_values_data:
    fetched_filename = 'fetched_data_values.json'

    try:
        with open(fetched_filename, 'w') as json_file:
            json.dump(data_values_data, json_file, indent=2)
        logging.info(f'Successfully stored fetched data from {source_dhis2_url} to {fetched_filename}')
    except Exception as e:
        logging.error(f'Failed to write fetched data to {fetched_filename}: {e}')
else:
    logging.error('No data fetched to store')

# Transform and sum data values to target DHIS2
transformed_data_values = {}
for value in data_values_data.get('dataValues', []):
    morezm_dataid = value['dataElement']
    morezm_categoryoptioncomboid = value['categoryOptionCombo']
    period = value['period']
    
    # Find the mapping row
    mapping_row = mappings_df[(mappings_df['morezm_dataid'] == morezm_dataid) & 
                              (mappings_df['morezm_categoryoptioncomboid'] == morezm_categoryoptioncomboid)]
    
    if not mapping_row.empty:
        target_data_element = mapping_row.iloc[0]['hia2_dataid']
        target_category_option_combo = mapping_row.iloc[0]['hia2_categoryoptioncomboid']
    else:
        logging.warning(f'Missing mapping for data element: {morezm_dataid}, category option combo: {morezm_categoryoptioncomboid}')
        target_data_element = 'unknown_dataelement'
        target_category_option_combo = 'unknown_categorycombo'
    
    target_org_unit = org_unit_mapping.get(value['orgUnit'], 'unknown_orgunit')

    key = (target_data_element, target_org_unit, target_category_option_combo, period)
    
    if key not in transformed_data_values:
        transformed_data_values[key] = 0
    transformed_data_values[key] += int(value['value'])

# Convert transformed data values to the required structure
payload = {
    "dataValues": [
        {
            "dataElement": key[0],
            "orgUnit": key[1],
            "categoryOptionCombo": key[2],
            "period": key[3],
            "value": total_value
        } for key, total_value in transformed_data_values.items()
    ]
}

filename = 'transformed_data_values_v2_tt23.json'

# Store the payload in a JSON file
try:
    with open(filename, 'w') as json_file:
        json.dump(payload, json_file, indent=2)
    logging.info(f'Successfully stored transformed data from {source_dhis2_url} to {filename}')
except Exception as e:
    logging.error(f'Failed to write transformed data to {filename}: {e}')

json_payload = json.dumps(payload)

# Set headers for JSON content
headers = {'Content-Type': 'application/json'}

# Send the POST request
try:
    response = requests.post(target_dhis2_url, auth=HTTPBasicAuth(target_dhis2_username, target_dhis2_password), headers=headers, data=json_payload, verify=cert_path)
    response.raise_for_status()
    logging.info(f'Successfully sent data to target DHIS2 {target_dhis2_url} for period: {period}. Status code: {response.status_code}')
    logging.info(response.json())
except requests.exceptions.RequestException as e:
    logging.error(f'Failed to send data to target DHIS2: {e}')
