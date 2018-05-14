import csv
import io
import requests
import requests_cache
import zipfile


class QuandlApi():

    def __init__(self, api_key, cache_path=None):
        self.base_url = 'https://www.quandl.com/api/v3'
        self.api_key = api_key
        #/databases/EOD/codes?api_key=YOURAPIKEY
        if cache_path:
            requests_cache.install_cache(cache_path)

    def get(self, endpoint, params=None):
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        url = self.base_url + endpoint
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp

    def get_databases(self):
        databases = []
        current_page = 1
        while True:
            rsp = requests.get(self.base_url + '/databases?current_page={}'.format(current_page))
            rsp.raise_for_status()
            json = rsp.json()
            databases.extend(json['databases'])
            meta = json['meta']
            if not meta['next_page']:
                break
            current_page += 1
        return databases


    def get_datasets(self, database):
        codes = []
        endpoint = '/databases/{}/codes'.format(database)
        resp = self.get(endpoint)

        zipped_stream = io.BytesIO(resp.content)
        zip_archive = zipfile.ZipFile(zipped_stream, 'r')
        csv_filename = zip_archive.namelist()[0]
        csv_string = zip_archive.read(csv_filename).decode('utf-8')
        csv_stream = io.StringIO(csv_string)
        csv_reader = csv.reader(csv_stream)
        for row in csv_reader:
            codes.append(row)
        return codes
