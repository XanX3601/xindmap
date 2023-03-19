import importlib
import inspect
import logging

from .Plugin import Plugin
from .PluginImportError import PluginImportError


class PluginImporter:
    # constructor **************************************************************
    def __init__(self):
        self.__plugins = {}

    # plugin *******************************************************************
    def import_plugins_from_module(self, module_name):
        module = importlib.import_module(module_name)

        classes = inspect.getmembers(module, inspect.isclass)
        classes = [c for c in classes if issubclass(c[1], Plugin)]

        imported_plugins = []

        for plugin_class_name, plugin_class in classes:
            plugin_name = f"{module_name}.{plugin_class_name}"

            if plugin_name in self.__plugins:
                raise PluginImportError(f"plugin {plugin_name} already imported")

            plugin = plugin_class()
            self.__plugins[f"{module_name}.{plugin_class_name}"] = plugin

            imported_plugins.append(plugin)

        return imported_plugins

    @property
    def plugins(self):
        return self.__plugins.values()
