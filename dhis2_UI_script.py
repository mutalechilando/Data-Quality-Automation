### Full Script with Tkinter UI

import os
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json
import logging
import tkinter as tk
from tkinter import messagebox, ttk

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

# Load credentials from file
credentials_file = 'credentials.txt'
credentials = read_credentials(credentials_file)

# Configuration for DHIS2 instances
source_dhis2_url = credentials.get('SOURCE_DHIS2_URL', 'https://lpho.more-zm.org:8445/api/29')
target_dhis2_url = credentials.get('TARGET_DHIS2_URL', 'https://train.moh.gov.zm/lions/api/29/dataValueSets')
source_dhis2_username = credentials.get('SOURCE_DHIS2_USERNAME', 'admin')
source_dhis2_password = credentials.get('SOURCE_DHIS2_PASSWORD', 'district')
target_dhis2_username = credentials.get('TARGET_DHIS2_USERNAME', 'admin')
target_dhis2_password = credentials.get('TARGET_DHIS2_PASSWORD', 'district')

# Function to load mappings from Excel file
def load_mappings(file_path, sheet_name=None):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df
    except Exception as e:
        logging.error(f'Error loading mappings: {e}')
        return pd.DataFrame()

# Load Org Units from the Excel file
file_path = 'mappings_v1.xlsx'
org_unit_df = load_mappings(file_path, sheet_name='org_units')

# Extract Org Units for the dropdown
org_unit_list = org_unit_df['MORE-ZM'].dropna().unique().tolist()

# Function to fetch data from DHIS2
def fetch_from_dhis2(url, username, password):
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password), headers={'Accept': 'application/json'}, verify=False)
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

# Main function to run the script
def run_script():
    org_unit_id = org_unit_var.get()
    period = period_entry.get()

    logging.info(f'Selected Org Unit: {org_unit_id}')
    logging.info(f'Entered Period: {period}')

    if not org_unit_id or not period:
        messagebox.showerror("Input Error", "Please select an Org Unit and enter a Period.")
        return

    dataset_id = 'N5mFDIePHXA'  # Replace with your actual dataset ID

    # Load mappings from the Excel file
    mappings_df = load_mappings(file_path, sheet_name='HIA2_MOREZM')
    org_unit_mapping = load_mappings(file_path, sheet_name='org_units').set_index('MORE-ZM')['HIA2'].to_dict()

    # Fetch data values from source DHIS2 (filtered by data element)
    data_values_url = f'{source_dhis2_url}/dataValueSets?orgUnit={org_unit_id}&period={period}&dataSet={dataset_id}&paging=false'
    data_values_data = fetch_from_dhis2(data_values_url, source_dhis2_username, source_dhis2_password)

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
        return

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
        
        try:
            int_value = int(value['value'])
        except ValueError:
            logging.warning(f'Non-numeric value encountered: {value["value"]} for data element {morezm_dataid}')
            continue  # Skip this value and move to the next

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
        return

    json_payload = json.dumps(payload)

    # Set headers for JSON content
    headers = {'Content-Type': 'application/json'}

    # Send the POST request
    try:
        response = requests.post(target_dhis2_url, auth=HTTPBasicAuth(target_dhis2_username, target_dhis2_password), headers=headers, data=json_payload, verify=False)
        response.raise_for_status()
        logging.info(f'Successfully sent data to target DHIS2 {target_dhis2_url} for period: {period}. Status code: {response.status_code}')
        logging.info(response.json())
        messagebox.showinfo("Success", "Data sent successfully!")
    except requests.exceptions.RequestException as e:
        logging.error(f'Failed to send data to target DHIS2: {e}')
        messagebox.showerror("Error", f"Failed to send data: {e}")

# Create the main window
root = tk.Tk()
root.title("DHIS2 Data Transfer")

# Org Unit ID dropdown
tk.Label(root, text="Org Unit ID").grid(row=0, column=0)
org_unit_var = tk.StringVar(root)
org_unit_dropdown = ttk.Combobox(root, textvariable=org_unit_var, values=org_unit_list, width=47)
org_unit_dropdown.grid(row=0, column=1)

# Period input
tk.Label(root, text="Period").grid(row=1, column=0)
period_entry = tk.Entry(root, width=50)
period_entry.grid(row=1, column=1)

# Run button
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=2, columnspan=2)

# Start the Tkinter event loop
root.mainloop()




### How It Works:

#1. **UI Components**: 
#   - **Source URL/Target URL**: Inputs for the source and target DHIS2 URLs.
#   - **Source/Target Username and Password**: Inputs for the credentials.
#   - **Run Script Button**: Button to execute the script.
#
#2. **Script Execution**: When you click the "Run Script" button, the `run_script` function collects all inputs and runs your DHIS2 data transfer script with these inputs.
#
#3. **Logging and Feedback**: The script logs the progress and outcomes, and it also shows message boxes for success or error states.
#
#### Customization:
#- **Replace Placeholder Values**: Replace placeholders such as `org_unit_id`, `period`, `dataset_id`, and paths to your actual values.
#- **Error Handling**: Additional error handling can be added as needed.
#
#This setup gives you a simple UI for configuring and running your script with custom credentials and URLs.