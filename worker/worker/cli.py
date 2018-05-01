"""
ledge.cli
~~~~~~~~~

This module implements the cli interface for the "ledge" cli application

"""
import click
import requests
import config
import yaml


@click.group()
def cli():
    pass

@click.command()
@click.option('--host', '-h', help="the edge's master host address")
def register(host):
    """Connect to a lambda edge network by providing the master host address"""

    # send CREATE connections to the master host
    r = requests.post(url=host+'/workers/')

    # if the connection is accepted, store the host information to ~/.ledge/config.yaml
    if r.status_code == 200:
        config.set('MASTER_HOST', host)
        print("Connected")
        print(config.get('MASTER_HOST'))
    # handle error
    else:
        print("Error: can't connect to the master host")

cli.add_command(register)

if __name__ == '__main__':
    cli()
