import requests
from requests.auth import HTTPBasicAuth
import json

# Configuration for DHIS2 instance
dhis2_url = 'https://lpho.more-zm.org:8445/api/29'
username = 'mchilando'
password = 'Chanda@10112020'
dataset_id = 'N5mFDIePHXA'

# API endpoint for the dataset
dataset_endpoint = f'/dataSets/{dataset_id}'

# Function to fetch dataset
def get_dataset(dhis2_url, username, password, dataset_id):
    url = f'{dhis2_url}{dataset_endpoint}'
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password), headers={'Accept': 'application/json'}, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Failed to fetch dataset. Status code: {response.status_code}')
            print(response.text)
            return {}
    except requests.exceptions.SSLError as e:
        print(f'SSL Error: {e}')
        return {}
    except Exception as e:
        print(f'Error fetching dataset: {e}')
        return {}

# Fetch dataset from DHIS2
dataset = get_dataset(dhis2_url, username, password, dataset_id)

# Save dataset to JSON file
if dataset:
    with open('dataset.json', 'w') as f:
        json.dump(dataset, f, indent=2)
    print('Dataset saved to dataset.json')
else:
    print('No dataset to save')
