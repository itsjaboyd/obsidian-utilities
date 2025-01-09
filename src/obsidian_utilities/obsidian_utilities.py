import click
from templates import copy_template
import pathlib
from configuration import configuration

@click.command()
@click.argument("filename", required=True, type=click.Path(dir_okay=False, path_type=pathlib.Path))
@click.argument("destination", required=True, type=click.Path(dir_okay=True, path_type=pathlib.Path))
@click.option("--uf", "--use-formatting", is_flag=True, default=False, help="Use formatting found in the destination.")
@click.option("--n", "--number-copies", type=int, default=1, help="Number of template copies to make.")
def copy_template(filename, destination, uf, n):
    """Copy a template file location to a directory."""

    usable_filename = filename
    configured_template_directory = False
    config = configuration.get_configuration()
    if not filename.exists() and str(filename) == filename.name:
        template_path = config.get("TEMPLATE", "directory", fallback=None)
        if template_path:
            usable_filename = pathlib.Path(template_path) / filename
            configured_template_directory = True

    result = False
    click.echo(f"Copying template file {filename.name} {n} time(s) to {destination.name}/.")
    try:
        result = copy_template.copy_template(usable_filename, destination, use_formatting=uf, number_copies=n)
    except FileExistsError as fee:
        click.echo(f"Cannot copy template file to destination: {fee}")
    click.echo(f"Results from copying template file: {result}")

    if not configured_template_directory:
        confirm_message = f"Would you like to set the default template directory to {filename.parent}?"
        if click.confirm(confirm_message):
            configuration.update_configuration("TEMPLATE", "directory", str(filename.parent.resolve()))
    

