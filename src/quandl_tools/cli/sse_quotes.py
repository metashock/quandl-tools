import argparse
import quandl
import sys
import termcolor


from quandl_tools.config import (
    Config,
)


from pdb import set_trace as bp


class SseQuotesCommand():

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

    def _colorize_change(self, a, b):
        if a is None or a == b:
            return str(b)
        elif a < b:
            return termcolor.colored(b, 'green')
        else:
            return termcolor.colored(b, 'red')

    def print_quotes(self, df):
        columns = [ 'High', 'Low', 'Last', 'Previous Day Price', 'Volume' ]
        widths = {}
        prev_close = None
        prev_volume = None

        for index, row in df.iterrows():
            close = row['Last']
            volume = row['Volume']
            print_close = self._colorize_change(prev_close, close)
            print_volume = self._colorize_change(prev_volume, volume)
            prev_close = close
            prev_volume = volume
            line = '{} {} {}'
            line = line.format(index, print_close, print_volume)
            print(line)

    def main(self):
        args = self.parse_args()
        config = Config.load()

        dataset = 'SSE/' + args.dataset
        #: str or list, depending on single dataset usage or multiset usage
        #    Dataset codes are available on the Quandl website
        params = {
            'api_key': config['quandl']['api_key'],
            'start_date': None,
            'end_date': None,
            'collapse': args.collapse,
            'rows': args.rows,  # Number of rows which will be returned
            'order': 'asc', # options are asc, desc. Default: `asc`
            'returns': None,
        }
        try:
            df = quandl.get(dataset, **params)
        except Exception as e:
            raise
            print('Error: ' + args.symbol)
            return 1

        self.print_quotes(df)


def main():
    return SseQuotesCommand().main()
