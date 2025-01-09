import click
from templates import copy_template as ct
import pathlib
from configuration import configuration as cfg

@click.command()
@click.argument("filename", required=True, type=click.Path(dir_okay=False, path_type=pathlib.Path))
@click.argument("destination", required=True, type=click.Path(dir_okay=True, path_type=pathlib.Path))
@click.option("--uf", "--use-formatting", is_flag=True, default=False, help="Use formatting found in the destination.")
@click.option("--n", "--number-copies", type=int, default=1, help="Number of template copies to make.")
def copy_template(filename, destination, uf, n):
    """Copy a template file location to a directory."""

    usable_filename = check_template_configuration(filename)
    result = False
    click.echo(f"Copying template file {filename.name} {n} time(s) to {destination.name}/.")
    try:
        result = ct.copy_template(usable_filename, destination, use_formatting=uf, number_copies=n)
    except FileExistsError as fee:
        click.echo(f"Cannot copy template file to destination: {fee}")
    except FileNotFoundError as fnfe:
        click.echo(f"Cannot find template file: {fnfe}")
    click.echo(f"Results from copying template file: {result}")
    

def check_template_configuration(template_file):
    just_filename = str(template_file) == template_file.name
    if template_file.is_file() and not just_filename:
        return template_file
    
    configuration = cfg.get_configuration()
    configured_template_path = configuration.get("TEMPLATE", "directory", fallback=None)
    if configured_template_path:
        return configured_template_path / template_file
    
    if not configured_template_path and not just_filename:
        confirm_message = f"Would you like to set the default template directory to {template_file.parent}?"
        if click.confirm(confirm_message):
            cfg.update_configuration("TEMPLATE", "directory", str(template_file.parent.resolve()))
    return template_file
    