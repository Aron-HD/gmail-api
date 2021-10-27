import logging
import click
import yaml
from logging.config import dictConfig
from pathlib import Path

from gmail.factory import main as gmail_main


def setup_logging():
    # create log directory if it doesn't exist
    try:
        Path('logs').mkdir(parents=True)
    except FileExistsError:
        pass

    # read in config for logging
    with open('logging.yml') as fin:
        config = yaml.safe_load(fin)

    dictConfig(config)


setup_logging()
log = logging.getLogger(__name__)
log.debug('\n\n# New run\n\nsetup logging')


@click.command()
@click.option(
    '-p', '--path',
    required=False,
    show_default=True,
    # default='logs',
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True,
        resolve_path=True
    ),
    help="The directory or file you wish to operate on.",
)
def cli(path):
    """
    Click command line pkg.
    """

    try:
        log.info(f'cli input: {path}')

        res = gmail_main()

        log.info('FINISHED')
    except Exception as e:
        raise e


if __name__ == '__main__':
    cli()
