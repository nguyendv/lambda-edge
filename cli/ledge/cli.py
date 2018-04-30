"""
ledge.cli
~~~~~~~~~

This module implements the cli interface for the "ledge" cli application

"""
import click
import requests
import config


@click.group()
def cli():
    pass

@click.command()
@click.option('--host', '-h', help="the edge's master host address")
def connect(host):
    """Connect to a lambda edge network by providing the master host address"""

    # send CREATE connections to the master host
    r = requests.post(url=host+'/connections/')

    # if the connection is accepted, store the host information to ~/.ledge/config.yaml
    if r.status_code == 200:
        config.set('MASTER_HOST', host)
        print("Connected")
        print(config.get('MASTER_HOST'))
    # handle error
    else:
        print("Error: can't connect to the master host")

@click.command()
def upload(fpath, config):
    """Upload a lambda function by providing its path and its config file"""
    print("uploading...")

@click.command()
def execute(id, args):
    """Execute a lambda function by providing the its id and arguments"""
    print("executing...")


cli.add_command(connect)
cli.add_command(upload)
cli.add_command(execute)

if __name__ == "__main__":
    cli()

