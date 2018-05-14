import setuptools
import sys

sys.path.insert(0, "src")
from quandl_tools import __version__
sys.path.remove("src")


setuptools.setup(name='quandl-tools',
    version=__version__,
    long_description='No long description',
    description='cli tools for the Quandl API',
    author='Thorsten Heymann',
    author_email='<hek2mglo@metashock.net>',
    package_dir={'': 'src'},
    packages=[
        'quandl_tools',
        'quandl_tools.cli',
    ],
    platforms='All',
    entry_points={'console_scripts': [
        'quandl-quotes = quandl_tools.cli.quotes:main',
        'quandl-dbs = quandl_tools.cli.dbs:main',
        'quandl-datasets = quandl_tools.cli.show_datasets:main',
        'sse-quotes = quandl_tools.cli.sse_quotes:main',
    ]}
)
