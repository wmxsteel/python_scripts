import os
from pyairtable import Api
import yaml
from pathlib import Path
import tabulate
import app_pathing as app_pathing

access_token = 'patIYkbz7EJtvqVz7.67b14ded621c16e6fe09cd3eca7ed92752d6104453c918203363d676c30b3bfc'

pathing = app_pathing.pathing_module()

path_config = pathing.get_path("config")

config_file = Path("app_config.yaml")

config_path = path_config / config_file

with open(config_path, 'r') as file:
    data = yaml.safe_load(file)

airtable_base_key = 'apppQnxGpHVwsyuNG'
airtable_api_key = data['airtable']['base_key']
headers = ''
api = Api(api_key=access_token)
headers = ['Address', 'Name', 'Units', 'Description']
table = api.table(airtable_base_key, 'ASIDictionary')
table.
print(tabulate.tabulate(table.all(), headers=headers, tablefmt="pretty"))
