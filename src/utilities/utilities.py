"""
    This module provides the command line functions that bring together the 
    obsidian utility functionality. The command line interface is built using 
    the Click library, which provides a simple and easy-to-use interface for 
    Python command line applications.

    Author: Jason Boyd
    Date: January 6, 2025
    Modified: January 14, 2025
"""

import click
import pathlib
from templates import copy_template as ct
from templates import templates as tp
from configuration import configuration as cf


@click.command()
@click.option(
    "-dir",
    "--directory",
    default=None,
    required=False,
    type=click.Path(dir_okay=True, path_type=pathlib.Path),
    help="Use a supplied directory to obtain directory information.",
)
@click.option(
    "-uc",
    "--use-config",
    default="templates",
    show_default=True,
    required=False,
    help="Use a saved path in configuration to obtain directory information.",
)
def directory_list(directory, use_config):
    """Given the options of supplying a directory or using a configuration key
        in PATHS, call the handle function to create and echo the analyzed directory.

    Args:
        directory (pathlib.Path): the path-like object to create the table list from.
        use_config (str): the optional key to give configuration for a path in
            the PATHS section (defaults to templates).
    """

    if directory is not None:
        handle_directory_list(directory)
        return

    config = cf.Configuration()
    directory_path = config.get_configuration()["PATHS"][use_config]
    handle_directory_list(directory_path)


def handle_directory_list(directory):
    """Handle calling the create_directory_table from the supplied directory.

    Args:
        directory (pathlib.Path): the directory to analyze and built the table from.
    """

    try:  # attempt to print the neat table information for directory
        result = tp.create_directory_table(directory)
        click.echo(result)
    except:  # some exception was raised in the table generation process
        click.echo(
            f"Cannot gather information as directory does not exist: '{directory}'"
        )


@click.command()
@click.argument(
    "filename", required=True, type=click.Path(dir_okay=False, path_type=pathlib.Path)
)
@click.argument(
    "destination", required=True, type=click.Path(dir_okay=True, path_type=pathlib.Path)
)
@click.option(
    "-uf",
    "--use-formatting",
    is_flag=True,
    default=False,
    help="Use formatting found in the destination.",
)
@click.option(
    "-n",
    "--number-copies",
    type=int,
    default=1,
    help="Number of template copies to make.",
)
def copy_template(filename, destination, use_formatting, number_copies):
    """Command to copy a template filename to a destination number_copies times with option use
        formatting use_formatting. The function checks template configuration to get a usable
        target directory from destination and attempts the copy operation.

    Args:
        filename (pathlib.Path): the template filename to copy from.
        destination (pathlib.Path): the target directory to put copies in.
        use_formatting (bool): analyze destination for formatting to use in the copy.
        number_copies (int): the number of copies to make of the template file.
    """

    results, usable_filename = [False], check_template_configuration(filename)
    expected_copies = ct.calculate_copied_paths(
        usable_filename, destination, use_formatting, number_copies
    )
    copies_verification = ct.verify_copies_target(expected_copies)
    if not copies_verification["valid"]:
        click.echo(f"Warning: {copies_verification['message']}")
        for existing_file in copies_verification["files"]:
            click.echo(f"\t- {existing_file}")
        confirm_message = "Would you like to continue copying the available files?"
        if not click.confirm(confirm_message):
            click.echo("Aborting copy operation.")
            return

    try:  # attempt to copy the template file to the destination using templates module
        click.echo(
            f"Copying template file '{filename.name}' {number_copies} time(s) to {destination.name}/."
        )
        results = ct.copy_template(
            usable_filename,
            destination,
            use_formatting=use_formatting,
            number_copies=number_copies,
        )
    except FileExistsError as fee:
        click.echo(f"Cannot copy template file to destination: {fee}")
    except FileNotFoundError as fnfe:
        click.echo(f"Cannot find template file location: {fnfe}")
    results_message = (
        f"Template file '{filename.name}' copied {'' if all(results) else 'un'}"
        f"successfully {number_copies} time(s) to {usable_filename}."
    )
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

    config = cf.Configuration()
    configured_template_path = config.get_configuration()["PATHS"]["templates"]
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
                config.update_configuration("PATHS", "templates", template_parent_path)
            handled_template_configuration = True
        # if the configured template path and suppled template path don't match, ask to update
        if (
            configured_template_path != template_parent_path
            and not handled_template_configuration
        ):
            confirm_message = f"Would you like to update the default template directory to {template_parent_path}?"
            if click.confirm(confirm_message):
                config.update_configuration("PATHS", "templates", template_parent_path)
    return template_file
