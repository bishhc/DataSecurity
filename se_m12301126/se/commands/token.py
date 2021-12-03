import click
import pathlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def read_key(path):
    f = open(path, 'rb')
    value = f.read()
    f.close()
    return value

@click.command()
@click.option('--keyword', type=str, help='keyword to search')
@click.option('--sk_prf', default='./data/sk_prf.txt', type=str, help='location of the prf secret key')
@click.option('--token_loc', default='./data/token.txt', type=str,
              help='location that the token generated will be saved')
def cli(keyword, sk_prf, token_loc):
    # load in key
    loc_sk_prf = pathlib.Path(sk_prf)
    key_prf = read_key(loc_sk_prf)

    # Set up cipher
    cipher_prf = AES.new(key_prf, AES.MODE_ECB)
    encoded_keyword = keyword.encode('utf-8')
    gen_token = cipher_prf.encrypt(pad(encoded_keyword, AES.block_size)).hex()

    click.echo("Inputted token is ", nl=False)
    click.echo(keyword)
    click.echo("Generated token is ", nl=False)
    click.echo(gen_token)

    loc_token = pathlib.Path(token_loc)
    f = open(loc_token, 'w')
    f.write(gen_token)
    f.close()
