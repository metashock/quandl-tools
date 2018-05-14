import argparse
import sys


from quandl_tools.config import (
    Config,
)
from quandl_tools.quandl_api import (
    QuandlApi,
)


from pdb import set_trace as bp
from pprint import pprint as pp


class ListDatabasesCommand():

    def parse_args(self):
        short_desc = 'List Quandle Databases'
        parser = argparse.ArgumentParser(short_desc)
        parser.add_argument('-f', '--free', action='store_true')
        parser.add_argument('-j', '--json', action='store_true')
        return parser.parse_args()

    def print_db(self, record):
        print('\t'.join([
            record['name'],
            record['database_code'],
            'premium' if record['premium'] else 'free',
        ]))

    def print_summary(self, n, free=False):
        free = 'free ' if free else ''
        print('\n {} {}databases found'.format(n, free))

    def main(self):
        args = self.parse_args()
        config = Config.load()

        api_key = config['quandl']['api_key']
        cache_path = config['quandl']['cache_folder'] + '/quandl_cache'
        api = QuandlApi(api_key, cache_path)
        databases = api.get_databases()
        if args.json:
            import json
            print(json.dumps(databases))
            return

        n = 0
        for database in sorted(databases, key=lambda x: x['database_code']):
            if args.free and database['premium']:
                continue
            n += 1
            self.print_db(database)
        
        self.print_summary(n, args.free)

def main():
    return ListDatabasesCommand().main()
