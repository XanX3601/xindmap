import click
import os

@click.command()
@click.argument(
    'filename',
    required=False,
    type=click.Path(exists=True),
    default=None
    )
@click.option(
    '--config-file',
    type=click.Path(exists=True),
    help='the config file to open',
    default='{}/.config/xindmap/xindmap.config'.format(os.path.expanduser('~'))
    )
def main(filename, config_file):
    import importlib.resources as pkg_resources
    import kivy.lang.builder
    import xindmap.view
    import xindmap.view.config
    import xindmap.view.resources

    os.environ['KIVY_NO_ARGS'] = '1'

    # load kv file
    with pkg_resources.path(xindmap.view.resources, 'xindmap.kv') as kv_file:
        kivy.lang.builder.Builder.load_file(str(kv_file))

    # create app
    app = xindmap.view.XindmapApp(config_file)

    # init app
    app.init()

    # run app
    app.run()
