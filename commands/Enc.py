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
@click.option('--ct_file', default="./data/Ciphertext.txt", type=str, help='name of Ciphertext to be outputted')
def cli(sk, pln_txt, ct_file):
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
	IV = get_random_bytes(16)
	data = bytearray(raw_text, 'utf-8')
	# click.echo(type(data))

	# using AES.cbc
	cipher = AES.new(key, AES.MODE_CBC, IV)
	ct_bytes = cipher.encrypt(pad(data, AES.block_size))
	iv = b64encode(cipher.iv).decode('utf-8')
	ct = b64encode(ct_bytes).decode('utf-8')
	click.echo("Ciphertext: ", nl=False)
	click.echo(ct)
	click.echo("IV: ", nl=False)
	click.echo(iv)

	# Output Results
	loc_iv = pathlib.Path("./data/iv.txt")
	f = open(loc_iv, 'wb')
	f.write(IV)
	f.close()

	loc_ct = pathlib.Path(ct_file)
	f = open(loc_ct, 'wb')
	f.write(ct_bytes)
	f.close()