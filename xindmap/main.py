import logging
import pathlib

import rich.logging
import rich.traceback
import rich_click as click

import xindmap.app


@click.command()
@click.option(
    "--config-directory",
    "config_directory_path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="path to the config directory",
)
@click.option(
    "--data-directory",
    "data_directory_path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="path to the data directory",
)
@click.option(
    "--init-file",
    "init_file_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="path to the initialization file",
)
@click.argument(
    "file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    required=False,
)
def main(config_directory_path, data_directory_path, init_file_path, file):
    """Main function to run xindmap.

    Args:
        init_file_path:
            Path to the init file that is read before starting the application.
            This path is given to [pathlib.Path][].
    """
    logging.basicConfig(
        level="NOTSET",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[rich.logging.RichHandler()],
    )

    rich.traceback.install()

    home_directory_path = pathlib.Path.home()

    if data_directory_path is not None:
        data_directory_path = pathlib.Path(data_directory_path)
    else:
        data_directory_path = home_directory_path / ".local" / "share" / "xindmap"

        if not data_directory_path.exists():
            data_directory_path.mkdir(parents=True)

    if config_directory_path is not None:
        config_directory_path = pathlib.Path(config_directory_path)
    else:
        config_directory_path = home_directory_path / ".config" / "xindmap"

        if not config_directory_path.exists():
            config_directory_path.mkdir(parents=True)

    if init_file_path is not None:
        init_file_path = pathlib.Path(init_file_path)
    else:
        init_file_path = config_directory_path / "init"

        if not init_file_path.exists():
            init_file_path = None

    app = xindmap.app.XindmapApp(
        config_directory_path, data_directory_path, init_file_path
    )
    app.init(file)
    app.start()


if __name__ == "__main__":
    main()
