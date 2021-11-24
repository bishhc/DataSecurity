import sys
import json

import click
import pathlib
from base64 import b64encode
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

@click.command()
@click.option('--sk', default="./data/key.txt", type=str, help='name of secret key')
@click.option('--pln_txt', default="./data/plaintext.txt", type=str, help='name of plaintext to encrypt')
def cli(sk, pln_txt):
	# Read in the data
	loc_sk = pathlib.Path(sk)
	loc_pln_txt = pathlib.Path(pln_txt)

	f = open(loc_sk, 'rb')
	key = f.read()
	click.echo(str(key))
	f.close()

	f = open(loc_pln_txt, 'r')
	raw_text = f.read()
	f.close()
	click.echo(raw_text)

	#Generate IV of 16 bytes
	data = bytearray(raw_text, 'utf-8')

	# Create ECB Cipher
	cipher_ECB = AES.new(key, AES.MODE_ECB)
	
	# Create CBC Cipher
	# An IV is not generated in this case since pycryptodome will initialize one by default
	#
	# Link to documentation
	# https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html#cbc-mode
	cipher_CBC = AES.new(key, AES.MODE_CBC)

	for i in range(5):
		ct_bytes_ECB = cipher_ECB.encrypt(pad(data, AES.block_size))

		ct_bytes_CBC = cipher_CBC.encrypt(pad(data, AES.block_size))

		ct_CBC = b64encode(ct_bytes_CBC).decode('utf-8')
		click.echo("CBC Ciphertext: ", nl=False)
		click.echo(ct_CBC, nl=False)
		ct_ECB = b64encode(ct_bytes_ECB)
		click.echo("	ECB Ciphertext: ", nl="False")
		click.echo(ct_ECB)