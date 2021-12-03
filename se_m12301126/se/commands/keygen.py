import click
import pathlib
from Crypto.Random import get_random_bytes


@click.command()
@click.option('--sk_prf', default='./data/sk_prf.txt', type=str, help='name for new secret prf key')
@click.option('--sk_aes', default='./data/sk_aes.txt', type=str, help='name for new secret aes key')
def cli(sk_prf, sk_aes):
    key_prf = get_random_bytes(32)
    click.echo('PRF secret key is ', nl=False)
    click.echo(key_prf.hex())

    key_aes = get_random_bytes(32)
    click.echo('AES secret key is ', nl=False)
    click.echo(key_aes.hex())

    loc_sk_prf = pathlib.Path(sk_prf)
    f = open(loc_sk_prf, 'wb')
    f.write(key_prf)
    f.close()

    loc_sk_aes = pathlib.Path(sk_aes)
    f = open(loc_sk_aes, 'wb')
    f.write(key_aes)
    f.close()
