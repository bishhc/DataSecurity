import click
import pathlib
from base64 import b64encode


@click.command()
@click.option('--d', default=1, type=int, help='int value indicating difficulty')
@click.option('--target', default='./data/target.txt', type=str, help='name of target to be outputted')
def cli(d, target):
    # Validate the value of d
    d = int(d)

    default_target = float.fromhex("0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")

    # Create the target by shifting the default to the right d number of times
    bit_out = int(default_target) >> d

    print(f"Target is {hex(bit_out)}")

    # output results
    loc_target = pathlib.Path(target)
    f = open(loc_target, 'wb')
    f.write(bit_out.to_bytes(32, 'big'))
    f.close()
