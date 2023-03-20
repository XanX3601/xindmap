import logging
import pathlib

import rich.logging
import rich.traceback
import rich_click as click

import xindmap.app


@click.command()
@click.option(
    "--init-file",
    "init_file_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
)
def main(init_file_path):
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[rich.logging.RichHandler()],
    )

    rich.traceback.install()

    if init_file_path is not None:
        init_file_path = pathlib.Path(init_file_path)

    app = xindmap.app.XindmapApp(init_file_path)
    app.init()
    app.start()


if __name__ == "__main__":
    main()
