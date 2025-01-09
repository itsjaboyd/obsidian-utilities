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
    results, usable_filename = False, check_template_configuration(filename)
    click.echo(f"Copying template file {filename.name} {n} time(s) to {destination.name}/.")
    try:
        results = ct.copy_template(usable_filename, destination, use_formatting=uf, number_copies=n)
    except FileExistsError as fee:
        click.echo(f"Cannot copy template file to destination: {fee}")
    except FileNotFoundError as fnfe:
        click.echo(f"Cannot find template file: {fnfe}")
    click.echo(f"Results from copying template file: {results}")
    

def check_template_configuration(template_file):
    config = cfg.get_configuration()
    configured_template_path = config.get("TEMPLATE", "directory", fallback=None)
    just_filename_supplied = str(template_file) == template_file.name
    handled_template_configuration = False
    # if just a filename was supplied, then use configured template path / filename
    if just_filename_supplied:
        if configured_template_path and not template_file.exists():
            return configured_template_path / template_file
        return template_file
    
    # the template_file is a path and not just a filename
    if template_file.is_file():
        template_parent_path = str(template_file.parent.resolve())
        if not configured_template_path:
            confirm_message = f"Would you like to set the default template directory to {template_parent_path}?"
            if click.confirm(confirm_message):
                cfg.update_configuration("TEMPLATE", "directory", template_parent_path)
            handled_template_configuration = True
        # if the configured template path and suppled template path don't match, ask to update
        if configured_template_path != template_parent_path and not handled_template_configuration:
            confirm_message = f"Would you like to update the default template directory to {template_parent_path}?"
            if click.confirm(confirm_message):
                cfg.update_configuration("TEMPLATE", "directory", template_parent_path)
    return template_file