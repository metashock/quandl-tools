import argparse
import quandl
import sys


from quandl_tools.config import (
    Config,
)


from pdb import set_trace as bp


class QuotesCommand():

    def parse_args(self):
        short_desc = 'Get quotes from Quandl'
        parser = argparse.ArgumentParser(short_desc)
        parser.add_argument('dataset', metavar='DATASET')
        parser.add_argument('-s', '--start-date')
        parser.add_argument('-e', '--end-date')
        parser.add_argument('-r', '--rows', type=int, default=30)
        parser.add_argument('-c', '--collapse',
                            help='Options are daily, weekly, monthly, quarterly, annual')

        return parser.parse_args()

    def main(self):
        args = self.parse_args()
        config = Config.load()

        dataset = args.dataset.upper()
        #: str or list, depending on single dataset usage or multiset usage
        #    Dataset codes are available on the Quandl website
        params = {
            'api_key': config['quandl']['api_key'],
            'start_date': None,
            'end_date': None,
            'collapse': args.collapse,
            'rows': args.rows,  # Number of rows which will be returned
            'order': None, # options are asc, desc. Default: `asc`
            'returns': None,
        }
        try:
            df = quandl.get(dataset, **params)
        except Exception as e:
            raise
            print('Error: ' + args.symbol)
            return 1
        print(df)
        return 1


def main():
    return QuotesCommand().main()
