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
        short_desc = 'List Datasets in a Quandl Database'
        parser = argparse.ArgumentParser(short_desc)
        parser.add_argument('database')
        parser.add_argument('filter', nargs='?')
        return parser.parse_args()

    def print_dataset(self, d):
        print(' {}\t{}'.format(d[0], d[1]))

    def print_summary(self, n):
        print('\n {} datasets found'.format(n))

    def main(self):
        args = self.parse_args()
        config = Config.load()
        api_key = config['quandl']['api_key']
        cache_path = config['quandl']['cache_folder'] + '/quandl_cache'
        api = QuandlApi(api_key, cache_path)
        datasets = api.get_datasets(args.database.upper())
        datasets.sort(key=lambda x: x[0])
        n = 0
        for dataset in datasets:
            if args.filter:
                filter_lower = args.filter.lower()
                name_lower = dataset[1].lower()
                if filter_lower not in name_lower:
                    continue
            self.print_dataset(dataset)
            n += 1

        self.print_summary(n)

def main():
    return ListDatabasesCommand().main()
