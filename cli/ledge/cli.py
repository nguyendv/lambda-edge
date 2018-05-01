"""
ledge.cli
~~~~~~~~~

This module implements the cli interface for the "ledge" cli application

"""
import time
import click
import requests
import config
import yaml


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
@click.option('--fpath', '-f', help="path to the function file")
@click.option('--cpath', '-c', help='path to the config file')
def upload(fpath, cpath):
    """Upload a lambda function by providing its path and its config file"""

    # Read the config file
    with open(cpath, 'r') as f:
        conf = yaml.load(f)
        environment = conf['environment']
    
    # TODO: upload environment

    files = {'upload': open(fpath,'rb')}

    host = config.get('MASTER_HOST')
    r = requests.post(host + '/functions/', files=files)

    if r.status_code == 200:
        print(r.json()['id'])
    else:
        print('Uploading error')

@click.command()
@click.option('--id', help='lambda function id')
@click.option('--arg', help='argument for the lambda function')
def execute(id, arg):
    """Execute a lambda function by providing the its id and arguments"""
    
    # Get a gateway ip
    host = config.get('MASTER_HOST')
    r = requests.post(host + '/clients/')

    if r.status_code == 200:
        gateway_ip = r.json()['gateway']
    else:
        print('Error when trying to get a gateway')

    # Send execution request to the gateway
    gateway_host = 'http://' + gateway_ip + ':5001'
    argv = [arg]
    r = requests.post(gateway_host + '/tasks/', json={'id': id, 'argv': argv})
    if r.status_code == 200:
        print(r.json()['ret'])
    else:
        print('Error when trying to execute the lambda function')


cli.add_command(connect)
cli.add_command(upload)
cli.add_command(execute)

if __name__ == "__main__":
    cli()

