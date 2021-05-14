import os
import requests

# Fetching env vars
airtable_url = os.environ.get('AIRTABLE_URL')
airtable_token = os.environ.get('AIRTABLE_TOKEN')


class Api:
    def __init__(self):
        self.req = requests

    def prettify_data(self, data):
        users = []
        for rec in data['records']:
            users.append(rec['fields'])

        return users

    def get_students(self):
        req = self.req

        res = req.get(url=airtable_url,
                      headers={'Authorization': 'Bearer {}'.format(airtable_token)})

        return self.prettify_data(res.json())
