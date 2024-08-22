import requests
from requests.auth import HTTPBasicAuth
import json

# Configuration for DHIS2 instances
source_dhis2_url = 'https://lpho.more-zm.org:8445/api/29'
target_dhis2_url = 'https://target-dhis2-instance.org/api/29'
source_dhis2_username = 'mchilando'
source_dhis2_password = 'Chanda@10112020'
target_dhis2_username = 'your-username'
target_dhis2_password = 'your-password'

# Parameters for data push
org_unit_id = 'ncgkwcQrfmc'  # Replace with your actual org unit ID - This is Kanyama First Level in MORE-ZM
period = '202301'  # Replace with your actual period (e.g., '202301' for January 2023)
dataset_id = 'N5mFDIePHXA'  # Replace with your actual dataset ID

# Mappings for IDs (update as needed)
data_element_mapping = {
    'IaN588shABx':'xC1fdx2189O',  # MORE-ZM -> TX_CURR_N: Number of adults and children receiving ART,  HIA2 -> Currently on ART
    'FxrH5b7Kwzd':'VYFMiXIdhIj',  # MORE-ZM -> TX_NEW_N (Age/Sex/CD4): New on ART,   HIA2 -> Started on ART
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
    'GJCHyERVprb':'Etb79cTNmIK',
    'itXclHr9vJB':'Etb79cTNmIK',
    'EUirlrjeuyD':'Etb79cTNmIK',
    'EIxDf63fSBt':'Etb79cTNmIK',
    'XAUDdgj170r':'ZjHIkuvbhVC',
    'GmBpE9zgqjo':'ZjHIkuvbhVC',
    'JVdTocRuapv':'ZjHIkuvbhVC',
    'bmsdvgZhL9a':'ZjHIkuvbhVC',
    'TtbV5KkymgO':'GJ9gSSmJoIv',
    'i8bbJKb3z8R':'GJ9gSSmJoIv',
    'ZxYehH4G6RH':'GJ9gSSmJoIv',
    'TibW6J8dq1g':'GJ9gSSmJoIv',
    'PLJTakDdV53':'rj1w1Pq8jkf',
    'pTZb77gmpJz':'rj1w1Pq8jkf',
    'XPOD1V1yZGA':'rj1w1Pq8jkf',
    'XZxdFU0BXnr':'rj1w1Pq8jkf',
    'nYhFwVdn6yI':'C56tlhPFjfp',
    'OjFfksyFwEK':'C56tlhPFjfp',
    't54VfPcV3PO':'C56tlhPFjfp',
    'bLmQXInnErg':'C56tlhPFjfp',
    'GwqFTtx6ip8':'VZ2XN0ZxA6S',
    'Gg9PrPV60yB':'VZ2XN0ZxA6S',
    'gEb1hic9W0Q':'VZ2XN0ZxA6S',
    'HsAHzk4Vl93':'VZ2XN0ZxA6S',
    'A7m2VprIfX6':'P02eYTPt4dS',
    'gktTfKFS0Sb':'P02eYTPt4dS',
    'irRMizqKxB9':'P02eYTPt4dS',
    'mrHgn460UKd':'P02eYTPt4dS',
    'XiP8m5druie':'P02eYTPt4dS',
    'houroQ2eAg5':'P02eYTPt4dS',
    'AXnjVfNOyLp':'P02eYTPt4dS',
    'Sd4aQy26rFi':'P02eYTPt4dS',
    'NJS9FHKkt60':'P02eYTPt4dS',
    'bXmlF8U5S4Z':'P02eYTPt4dS',
    'yiTxxJGJhxq':'P02eYTPt4dS',
    'vHjUC2quHIh':'P02eYTPt4dS',
    'cwW9EdUW42T':'P02eYTPt4dS',
    'BmlMYjaD0f2':'P02eYTPt4dS',
    'kOekjv35NSc':'P02eYTPt4dS',
    'XbGS8645beG':'P02eYTPt4dS',
    'LZTUXn0IqPR':'P02eYTPt4dS',
    'ePzY27bUfOQ':'P02eYTPt4dS',
    'yCFBk4POCVE':'P02eYTPt4dS',
    'pXZ5ROopsKI':'P02eYTPt4dS',
    'DKslKgR6d24':'uIpRFk3Jgz6',
    'XNeukjQ33aR':'uIpRFk3Jgz6',
    'ar4LdDCb7ys':'uIpRFk3Jgz6',
    'uKjgMw1KB5x':'uIpRFk3Jgz6',
    'GK1aLrX9Ozl':'y01Z8E2MBYt',
    'vJyasWtD6XN':'y01Z8E2MBYt',
    'dEWS0fEmrGz':'y01Z8E2MBYt',
    'DdbOZH9RV9f':'y01Z8E2MBYt',
    'qJeSIcklDAj':'Y4YXc8CkgNT',
    'wqdPdnizqKf':'Y4YXc8CkgNT',
    'r9oEfpAaQZX':'Y4YXc8CkgNT',
    'Kcy4950N12q':'Y4YXc8CkgNT',
    'EA9bjxHaD1n':'Y4YXc8CkgNT',
    'bcIK2laAjds':'Y4YXc8CkgNT',
    'vO3jTSHcAHc':'Y4YXc8CkgNT',
    'gIxJ7P1RBz8':'Y4YXc8CkgNT',
    'vzjlODEf6wJ':'Y4YXc8CkgNT',
    'cIBIxHnMTHM':'Y4YXc8CkgNT',
    'a0rRJuL6vRR':'Y4YXc8CkgNT',
    'FXjBdlZqhPj':'Y4YXc8CkgNT',
    'b2Qx6QGVxhU':'KaUFNUYC7ft',
    'PiaQ0xhTgT1':'KaUFNUYC7ft',
    'cAH6F97fEDd':'KaUFNUYC7ft',
    'iwHIy31tXX2':'KaUFNUYC7ft',
    'w3nKqw2YsQ4':'WqDPWzWmlQT',
    'v6j4TfFZoHN':'WqDPWzWmlQT',
    'o5RYjQVKpga':'WqDPWzWmlQT',
    'BYKtAfPOV2G':'WqDPWzWmlQT',
    'kykToApavgl':'fzKC3XrqoHz',
    'aeJWFTAHHiC':'fzKC3XrqoHz',
    'f70hkVLAPWq':'fzKC3XrqoHz',
    'wNzYh5uPXHM':'fzKC3XrqoHz',
    'P4YutEStRDH':'Ak2FdPn5Q9G',
    'HSfTR7AJrhC':'Ak2FdPn5Q9G',
    'nqbBBu1xDjC':'Ak2FdPn5Q9G',
    'cYqPdGWmGYh':'Ak2FdPn5Q9G',
    'BfCfXOpMlzG':'puTb3F0KdEX',
    'K1dg7hKtlFp':'puTb3F0KdEX',
    'bckX8LQvszK':'puTb3F0KdEX',
    'uBk7sWecTIY':'puTb3F0KdEX',
    'KSkmoJyNj4X':'Qqla7AHVmyE',
    'koDAVVHmDZr':'Qqla7AHVmyE',
    'LfzRyjSBemZ':'Qqla7AHVmyE',
    'pYnOAMiLfO6':'Qqla7AHVmyE',
    'phDpNW1bYlY':'u3zNA6CU0aC',
    'fjbgqgCbc06':'u3zNA6CU0aC',
    'oDqENCEjiwI':'u3zNA6CU0aC',
    'kODNadwSjW1':'u3zNA6CU0aC',
    'W68fz8St38t':'u3zNA6CU0aC',
    'uC42raTt3Rh':'u3zNA6CU0aC',
    'fgfwx17TFxY':'u3zNA6CU0aC',
    'l1KIGJAzIlD':'u3zNA6CU0aC',
    'vzFJHCd6WSl':'u3zNA6CU0aC',
    'EIQzgGBaLqd':'u3zNA6CU0aC',
    'HmF9G9UF9Z5':'u3zNA6CU0aC',
    'RQqLlUYtGef':'u3zNA6CU0aC',
    'qXd9gcgF3A9':'u3zNA6CU0aC',
    'oqGw6F7ltAf':'u3zNA6CU0aC',
    'hfQ3KjWCOab':'u3zNA6CU0aC',
    'Gk56yOOfFfT':'u3zNA6CU0aC',
    'Mz5B6yCNdbR':'u3zNA6CU0aC',
    'pXcj1QUWlXN':'u3zNA6CU0aC',
    'kznygAJZeOk':'u3zNA6CU0aC',
    'QHvysmXYhFq':'u3zNA6CU0aC',
    'bpBhaMLEyKS':'CTYuhOgISwV',
    'VxEG3B2UpD2':'CTYuhOgISwV',
    'BYWCVXoBTFS':'CTYuhOgISwV',
    'yjBrNi80u9E':'CTYuhOgISwV',
    'DldbLcUGqZC':'oT9hPGqZ3pC',
    'oNDFPJ2GoJ4':'oT9hPGqZ3pC',
    'ugSdtjcV3Ka':'oT9hPGqZ3pC',
    'UvZoBfy42Qs':'oT9hPGqZ3pC',
    'DmmQOVH5K3D':'zqBB8YN5eze',
    'YHsEhoHrgUb':'zqBB8YN5eze',
    'DEyXaIYtENw':'zqBB8YN5eze',
    'TPiYG5Pc6ce':'zqBB8YN5eze',
    'ugfteUHoKZp':'zqBB8YN5eze',
    'Dc3O60zWKBQ':'zqBB8YN5eze',
    'OZOGHTRCigR':'zqBB8YN5eze',
    'YlbPFunlk1s':'zqBB8YN5eze',
    'v0F5fHeymMZ':'zqBB8YN5eze',
    'Qu1Sye9nhcT':'zqBB8YN5eze',
    'aj9DJdh47Hr':'zqBB8YN5eze',
    'x2ieZXGZl78':'zqBB8YN5eze',

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
data_values_url = f'{source_dhis2_url}/dataValueSets?orgUnit={org_unit_id}&period={period}&dataSet={dataset_id}&paging=false' #&filter=dataElement:{specific_data_element_id}
data_values_data = fetch_from_dhis2(data_values_url, source_dhis2_username, source_dhis2_password)

    # Filter for desired category option combo IDs
desired_category_combo_ids = ['Etb79cTNmIK','ZjHIkuvbhVC','GJ9gSSmJoIv','rj1w1Pq8jkf','C56tlhPFjfp','VZ2XN0ZxA6S','P02eYTPt4dS','uIpRFk3Jgz6','y01Z8E2MBYt','Y4YXc8CkgNT',
'KaUFNUYC7ft','WqDPWzWmlQT','fzKC3XrqoHz','Ak2FdPn5Q9G','puTb3F0KdEX','Qqla7AHVmyE','u3zNA6CU0aC','CTYuhOgISwV','oT9hPGqZ3pC','zqBB8YN5eze','zqBB8YN5eze','zqBB8YN5eze',
'u3zNA6CU0aC','u3zNA6CU0aC','u3zNA6CU0aC','u3zNA6CU0aC','u3zNA6CU0aC']  # Replace with your desired IDs


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
	
filename = 'transformed_data_values.json'

with open(filename, 'w') as json_file:
    json.dump(transformed_data_values, json_file)
    
print(f'Successfully stored transformed data to {filename}')





