import click

from magnascale_automation.command import CONTEXT_SETTINGS


@click.group(context_settings=CONTEXT_SETTINGS)
def web_service():
    """Web Service CLI.

    This is the main entry point for the web service CLI.
    """
    pass


@web_service.command(context_settings=CONTEXT_SETTINGS)
def run():
    click.echo("Start dallas web service")
