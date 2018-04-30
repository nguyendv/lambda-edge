import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--host', '-h', help="the edge's master host address")
def connect(host):
    """Connect to a lambda edge network by providing the master host address"""
    print("connecting...")

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

