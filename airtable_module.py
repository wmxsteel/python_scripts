import os
from pyairtable import Api
api = Api(api_key=os.environ['AIRTABLE_API_KEY'], base_key=os.environ['AIRTABLE_BASE_KEY'])
