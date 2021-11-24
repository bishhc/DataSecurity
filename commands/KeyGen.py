import sys

import click
import pathlib
from Crypto.Random import get_random_bytes

@click.command()
@click.option('--name', default="./data/key.txt", type=str, help='name for new secret key')
def cli(name):
	key = get_random_bytes(16)
	click.echo("Secret key is ", nl=False)
	click.echo(str(key))

	# TODO: Output this to a file.
	loc = pathlib.Path(name)
	f = open(loc, 'wb')
	f.write(key)
	f.close()