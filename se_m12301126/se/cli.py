import os
import sys

import click

class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(os.path.join(os.path.dirname(__file__), "commands")):
            if filename.endswith(".py") and not filename.startswith("__"):
                rv.append(filename.replace('.py', ''))
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"se.commands.{name}", None, None, ["cli"])
        except ImportError:
            return
        return mod.cli


@click.command(cls=ComplexCLI)
def cli():
	"""Welcome to se"""
	pass