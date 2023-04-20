"""Xindmap pluging module.

# `xindmap.plugin`

Plugins are objects that increase the capacity of the application.
They expose commands that can interact with the application through the
[api][xindmap.command.CommandApi.CommandApi].

Plugins are classed derived from [`Plugin`][xindmap.plugin.Plugin.Plugin][]
class.
They are imported at runtime using the
[plugin importer][xindmap.plugin.PluginImporter.PluginImporter].

## Module exported content

- [`xindmap.plugin.Plugin.Plugin`][]
- [`xindmap.plugin.PluginImporter.PluginImporter`][]
"""

from .Plugin import Plugin
from .PluginImporter import PluginImporter
