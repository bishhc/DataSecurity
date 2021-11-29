import click
import pathlib
from Crypto.Hash import SHA256


@click.command()
@click.option('--input', default='./data/input.txt', type=str, help='name of input to be inputted')
@click.option('--target', default='./data/target.txt', type=str, help='name of target to be inputted')
@click.option('--solution', default='./data/solution.txt', type=str, help='name of solution to be outputted')
def cli(input, target, solution):
    loc_input = pathlib.Path(input)
    f = open(loc_input, 'rb')
    message = f.read()
    f.close()

    loc_target = pathlib.Path(target)
    f = open(loc_target, 'rb')
    t_bytes = f.read()
    f.close()

    loc_solution = pathlib.Path(solution)
    f = open(loc_solution, 'rb')
    s = f.read()
    f.close()

    hash_of_message = SHA256.new(message)
    hash_of_message.update(s)

    result = hash_of_message.digest() < t_bytes
    if result:
        click.echo('The following is a valid solution')
        click.echo(hash_of_message.hexdigest())
    else:
        click.echo('The following is not a valid solution')
        click.echo(hash_of_message.hexdigest())
