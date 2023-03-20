import logging

import xindmap.plugin


class TestPlugin(xindmap.plugin.Plugin):
    def commands(self):
        return [("test", lambda api: logging.info("command test from test plugin"))]

    def __init__(self):
        super().__init__()
