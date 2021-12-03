import click
import pathlib
import json
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def read_key(path):
    f = open(path, 'rb')
    value = f.read()
    f.close()
    return value


@click.command()
@click.option('--cf_loc', default='./data/ciphertexts/c1.txt', type=str, help='name for new secret aes key')
@click.option('--sk_aes', default='./data/sk_aes.txt', type=str, help='name for new secret aes key')
def cli(cf_loc, sk_aes):
    loc_sk_aes = pathlib.Path(sk_aes)
    key_aes = read_key(loc_sk_aes)

    # loc_iv = pathlib.Path('./data/iv.txt')
    # iv = read_key(loc_iv)
    current_file = pathlib.Path(cf_loc)
    with open(current_file) as json_file:
        b64 = json.load(json_file)

        iv = b64decode(b64['iv'])
        ct = b64decode(b64['ciphertext'])
        cipher_cbc = AES.new(key_aes, AES.MODE_CBC, iv)
        pt = unpad(cipher_cbc.decrypt(ct), AES.block_size)

        print(pt)

    # Setup cipher
