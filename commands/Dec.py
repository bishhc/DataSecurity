import sys
import json

import click
import pathlib
from base64 import b64encode
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

@click.command()
@click.option('--sk', default="./data/key.txt", type=str, help='name of secret key')
@click.option('--ct_file', default="./data/Ciphertext.txt", type=str, help='name of plaintext to encrypt')
@click.option('--iv_file', default="./data/iv.txt", type=str, help='name of file holding iv')
@click.option('--result_loc', default="./data/results.txt", type=str, help='name of Ciphertext to be outputted')
def cli(sk, ct_file, iv_file, result_loc):
	# Read in the bit values from files
	loc_sk = pathlib.Path(sk)
	loc_ct_file = pathlib.Path(ct_file)
	loc_iv = pathlib.Path(iv_file)

	f = open(loc_sk, 'rb')
	key = f.read()
	f.close()
	click.echo(str(key))

	f = open(loc_ct_file, 'rb')
	ct = f.read()
	f.close()
	
	f = open(loc_iv, 'rb')
	iv = f.read()
	f.close()

	# using AES.cbc
	# Decrypt the ciphertext
	cipher = AES.new(key, AES.MODE_CBC, iv)
	pt = unpad(cipher.decrypt(ct), AES.block_size)


	click.echo("Plaintext: ", nl=False)
	click.echo(pt)

	# Output Results
	loc_results = pathlib.Path(result_loc)
	f = open(loc_results, 'w')
	f.write(str(pt))
	f.close()