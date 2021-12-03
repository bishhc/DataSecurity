import sys
import json
import timeit

import click
import pathlib
from base64 import b64decode
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

@click.command()
def cli():
	SETUP_CODE = '''
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
key = get_random_bytes(16)
data = b"Welcome to data security and privacy 2021"
cipher = AES.new(key, AES.MODE_CBC)
ct = cipher.encrypt(pad(data, AES.block_size))
cipher_2 = AES.new(key, AES.MODE_CBC)'''

	TEST_CODE = '''
ct = cipher.encrypt(pad(data, AES.block_size))'''
	
	times = timeit.repeat(setup=SETUP_CODE,stmt=TEST_CODE,repeat=3,number=10000)

	print('Encryption time: {} seconds'.format(times))
	print("\n")



	TEST_CODE = '''
pt = unpad(cipher_2.decrypt(ct), AES.block_size)'''
	
	times = timeit.repeat(setup=SETUP_CODE,stmt=TEST_CODE,repeat=3,number=10000)

	print('Decryption time: {} seconds'.format(times))