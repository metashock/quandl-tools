import os
import yaml
import logging


class Config(dict):

    @staticmethod
    def load():
        locations = [
            'quandl.yml',
            '{}/quandl.yml'.format(os.environ['HOME']),
            '/etc/quandl/quandl.yml',
        ]
        for filename in locations:
            try:
                with open(filename, 'r') as fd:
                    return Config(yaml.load(fd))
            except FileNotFoundError:
                pass

        raise Exception('Failed to load quandl.yml')
