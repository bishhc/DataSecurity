import click
import pathlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
from base64 import b64encode
import binascii


def read_key(path):
    f = open(path, 'rb')
    value = f.read()
    f.close()
    return value


@click.command()
@click.option('--sk_prf', default='./data/sk_prf.txt', type=str, help='name for new secret prf key')
@click.option('--sk_aes', default='./data/sk_aes.txt', type=str, help='name for new secret aes key')
@click.option('--index_loc', default='./data/index.txt', type=str, help='location where inverted index will be stored')
@click.option('--files_loc', default='./data/files', type=str, help='location of folder holding plaintext files')
@click.option('--cf_loc', default='./data/ciphertexts', type=str, help='location of folder holding ciphertext files')
def cli(sk_prf, sk_aes, index_loc, files_loc, cf_loc):
    # Read in keys
    loc_sk_prf = pathlib.Path(sk_prf)
    key_prf = read_key(loc_sk_prf)
    loc_sk_aes = pathlib.Path(sk_aes)
    key_aes = read_key(loc_sk_aes)

    # Create ciphers
    cipher_prf = AES.new(key_prf, AES.MODE_ECB)

    # Read all files in the files folder
    # Then load them into a pandas
    inverted_index = {}
    p = pathlib.Path(files_loc).glob('**/*')
    files = [x for x in p if x.is_file()]
    for index, file in enumerate(files):
        f = open(file)
        raw_content = f.read()
        f.close()

        output_path = pathlib.Path(cf_loc)
        output_path_2 = output_path.joinpath(f"c{index+1}.txt")
        f = open(output_path_2, 'w')

        raw_content_bytes = raw_content.encode('utf-8')
        cipher_cbc = AES.new(key_aes, AES.MODE_CBC)
        ct_bytes_cbc = cipher_cbc.encrypt(pad(raw_content_bytes, AES.block_size))
        iv = b64encode(cipher_cbc.iv).decode('utf-8')
        ct_cbc = b64encode(ct_bytes_cbc).decode('utf-8')
        result = json.dumps({'iv': iv, 'ciphertext': ct_cbc})
        f.write(result)

        # Process current content into inverted index
        terms = raw_content.split()
        for t in terms:
            # Encrypt t with prf
            # convert to bits
            t_bytes = t.encode('utf-8')
            ct_bytes = cipher_cbc.encrypt(pad(t_bytes, AES.block_size))
            iv = b64encode(cipher_cbc.iv).decode('utf-8')

            ii_hex = cipher_prf.encrypt(pad(t_bytes, AES.block_size)).hex()

            if ii_hex not in inverted_index:
                inverted_index[ii_hex] = []
            if ii_hex in inverted_index:
                inverted_index[ii_hex].append(f"c{index+1}.txt")

    print("The inverted index is :")
    for element in inverted_index:
        print(f"{element} : {inverted_index[element]}")

    loc_ii = pathlib.Path(index_loc)
    f = open(loc_ii, 'w')
    f.write(json.dumps(inverted_index))
    f.close()
