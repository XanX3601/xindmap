import importlib
import inspect

from .Plugin import Plugin
from .PluginImportError import PluginImportError


class PluginImporter:
    """Imports [plugins][xindmap.plugin.Plugin.Plugin] and stores them.

    For now [plugins][xindmap.plugin.Plugin.Plugin] can only be imported from
    a module name.

    Attributes:
        __plugins: A dictionnary mapping a plugin identifier to the plugin.
    """
    # constructor **************************************************************
    def __init__(self):
        """Instantiates this plugin importer.
        """
        self.__plugins = {}

    # plugin *******************************************************************
    def import_plugins_from_module(self, module_name):
        """Import all plugins found in a given module.

        Searches for all classes derived from
        [`Plugin`][xindmap.plugin.Plugin.Plugin] in a given module, instantiates
        one object from each and stores them.

        Plugins are then named base on the identifier of their class.

        Args:
            module_name:
                The name of the module from which import [plugins][xindmap.plugin.Plugin.Plugin].

        Returns:
            A list containing all plugins imported from the module.

        Raises:
            PluginImportError: If a found plugin has already been imported.
        """
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
        """Returns an iterator over all imported
        [plugins][xindmap.plugin.Plugin.Plugin].
        """
        return self.__plugins.values()
