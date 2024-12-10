import click

from magnascale_automation.command import CONTEXT_SETTINGS
from magnascale_automation.command.lisa.web_service import web_service


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    pass


main.add_command(web_service)
