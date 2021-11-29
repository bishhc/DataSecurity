import click
import pathlib
from Crypto.Hash import SHA256
import time


@click.command()
@click.option('--input', default='./data/input.txt', type=str, help='name of input to be inputted')
@click.option('--target', default='./data/target.txt', type=str, help='name of target to be inputted')
@click.option('--solution', default='./data/solution.txt', type=str, help='name of solution to be outputted')
def cli(input, target, solution):
    # Read in input from file
    loc_input = pathlib.Path(input)
    f = open(loc_input, 'rb')
    message = f.read()
    print("Value of message:")
    click.echo(message)
    f.close()

    # Read in target
    loc_target = pathlib.Path(target)
    f = open(loc_target, 'rb')
    t_bit = f.read()
    f.close()

    # Start timeout recording
    timeout = time.time() + 120 * 6
    # Start hashing
    hash_of_message = SHA256.new(message)

    s = 1
    h = hash_of_message.copy()
    h.update(s.to_bytes(32, byteorder='big'))
    # print('Value of t_bit:')
    # print(t_bit.hex())
    # print('Value of h')
    # print(h.hexdigest())
    # print(hash_of_message.hexdigest())

    print(h.digest() > t_bit)
    while (h.digest() > t_bit) and (time.time() < timeout):
        s += 1
        h = hash_of_message.copy()
        h.update(s.to_bytes(32, byteorder='big'))

    print('Value of t_bit:')
    print(t_bit.hex())
    print('Value of h')
    print(h.hexdigest())
    print('Value of S')
    print(s)
    print(f'Number of attempts: {s}')

    if time.time() > timeout:
        print("Solution timed out after 6 hours")
        return 0

    loc_solution = pathlib.Path(solution)
    f = open(loc_solution, 'wb')
    f.write(s.to_bytes(32, byteorder='big'))
    f.close()
    return 0
