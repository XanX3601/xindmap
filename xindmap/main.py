import logging
import rich.logging
import rich_click as click


@click.command()
def main():
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[rich.logging.RichHandler()],
    )
