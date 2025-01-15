"""
    This module provides the command line functions that bring together the 
    obsidian utility functionality. The command line interface is built using 
    the Click library, which provides a simple and easy-to-use interface for 
    Python command line applications.

    Author: Jason Boyd
    Date: January 6, 2025
    Modified: January 14, 2025
"""

# TODO:
# - [ ] Add a command to list all available templates in the template directory.
# - [ ] Provide unit testing for click application and command line functions.
# - [ ] Format package to PEP8 style using Black or some other automatic formatter.


import click
import pathlib
from templates import copy_template as ct
from configuration import configuration as cfg

@click.command()
@click.argument("filename", required=True, type=click.Path(dir_okay=False, path_type=pathlib.Path))
@click.argument("destination", required=True, type=click.Path(dir_okay=True, path_type=pathlib.Path))
@click.option("--uf", "--use-formatting", is_flag=True, default=False, help="Use formatting found in the destination.")
@click.option("--n", "--number-copies", type=int, default=1, help="Number of template copies to make.")
def copy_template(filename, destination, uf, n):
    """Command to copy a template filename to a destination n times with option use 
        formatting uf. The function checks template configuration to get a usable 
        target directory from destination and attempts the copy operation.

    Args:
        filename (pathlib.Path): the template filename to copy from.
        destination (pathlib.Path): the target directory to put copies in.
        uf (bool): analyze destination for formatting to use in the copy.
        n (int): the number of copies to make of the template file.
    """

    results, usable_filename = [False], check_template_configuration(filename)
    try: # attempt to copy the template file to the destination using templates module
        click.echo(f"Copying template file '{filename.name}' {n} time(s) to {destination.name}/.")
        results = ct.copy_template(usable_filename, destination, use_formatting=uf, number_copies=n)
    except FileExistsError as fee:
        click.echo(f"Cannot copy template file to destination: {fee}")
    except FileNotFoundError as fnfe:
        click.echo(f"Cannot find template file location: {fnfe}")
    results_message = (f"Template file '{filename.name}' copied {"" if all(results) else "un"}"
        f"successfully {n} time(s) to {usable_filename}.")
    click.echo(results_message)
    

def check_template_configuration(template_file):
    """Given a template file path, save or update template path configuration if 
        necessary and return a usable template location path based on what the 
        caller supplied; if just a filename, use configuration otherwise use 
        what the caller supplied as a template path.

    Args:
        template_file (pathlib.Path): the template file location to analyze 
            and possibly update configuration for.

    Returns:
        pathlib.Path: the usable path to copy the template file from.
    """
    
    configured_template_path = cfg.get_configuration().get("TEMPLATE", "directory", fallback=None)
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