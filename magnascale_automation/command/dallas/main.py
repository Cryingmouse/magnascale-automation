import click

from magnascale_automation.command import CONTEXT_SETTINGS
from magnascale_automation.command.interactive.menu import build_menu
from magnascale_automation.command.dallas.web_service import web_service


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


cli.add_command(web_service)


@cli.command(context_settings=CONTEXT_SETTINGS)
def run():
    """run cli in interactive mode."""
    menu_manager = build_menu()
    menu_manager.run()
