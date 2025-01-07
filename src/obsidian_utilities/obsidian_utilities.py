import click
import templates.copy_template
import pathlib

@click.command()
@click.argument("filename", required=True, type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path))
@click.argument("destination", required=True, type=click.Path(exists=True, dir_okay=True, path_type=pathlib.Path))
@click.option("--uf", "--use-formatting", is_flag=True, default=False, help="Use formatting found in the destination.")
@click.option("--n", "--number-copies", type=int, default=1, help="Number of template copies to make.")
def copy_template(filename, destination, uf, n):
    """Copy a template file location to a directory."""

    result = False
    click.echo(f"Copying template file {filename.name} {n} time(s) to {destination.name}/.")
    try:
        result = templates.copy_template.copy_template(filename, destination, use_formatting=uf, number_copies=n)
    except FileExistsError as fee:
        click.echo(f"Cannot copy template file to destination: {fee}")
    click.echo(f"Results from copying template file: {result}")