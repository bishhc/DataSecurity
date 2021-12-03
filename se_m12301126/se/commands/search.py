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
@click.option('--index_loc', default='./data/index.txt', type=str, help='location of the inverted index')
@click.option('--token_loc', default='./data/token.txt', type=str,
              help='location that the token generated will be saved')
@click.option('--cf_loc', default='./data/ciphertexts', type=str, help='folder that holds the ciphertext files')
@click.option('--sk_aes', default='./data/sk_aes.txt', type=str, help='name for new secret aes key')
def cli(index_loc, token_loc, cf_loc, sk_aes):
    loc_index = pathlib.Path(index_loc)
    with open(loc_index) as json_file:
        inverted_index = json.load(json_file)

    loc_token = pathlib.Path(token_loc)
    with open(loc_token) as token_file:
        keyword = token_file.read()
    print(inverted_index[keyword])

    loc_sk_aes = pathlib.Path(sk_aes)
    key_aes = read_key(loc_sk_aes)

    loc_iv = pathlib.Path('./data/iv.txt')
    iv = read_key(loc_iv)

    # Setup cipher
    cipher_aes = AES.new(key_aes, AES.MODE_CBC, iv)

    cipherfolder_path = pathlib.Path(cf_loc)
    for filename in inverted_index[keyword]:
        current_file = cipherfolder_path.joinpath(filename)
        with open(current_file) as json_file:
            b64 = json.load(json_file)

            iv = b64decode(b64['iv'])
            ct = b64decode(b64['ciphertext'])
            cipher_cbc = AES.new(key_aes, AES.MODE_CBC, iv)
            pt = unpad(cipher_cbc.decrypt(ct), AES.block_size)

            print(pt)
