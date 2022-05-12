import click

@click.command()
@click.option(
    '-log',
    '--log-level',
    default='debug',
    type=click.Choice(
        ['trace', 'debug', 'info', 'warning', 'error', 'critical'],
        case_sensitive=False
    )
)
def xindmap(log_level):
    import kivy.lang.builder as kbuilder
    import kivy.logger as klogger
    import importlib.resources as pkg_resources
    import xindmap.app as xapp
    import xindmap.logging as xlogging
    import xindmap.resources as xresources

    logger = klogger.Logger

    # set log level beforehand
    logger.setLevel(klogger.LOG_LEVELS[log_level])

    xlogging.info(
        '************************************* XINDMAP START **************************************'
    )

    with pkg_resources.path(xresources, 'xindmap.kv') as kv_file_path:
        kv_file_path = str(kv_file_path.resolve())

        builder = kbuilder.Builder
        builder.load_file(kv_file_path)

    xindmap_app = xapp.XindmapApp()
    xindmap_app.init()
    xindmap_app.run()

    xlogging.info(
        '************************************** XINDMAP END ***************************************'
    )

if __name__ == '__main__':
    xindmap()
