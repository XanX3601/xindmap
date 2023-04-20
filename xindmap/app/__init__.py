"""Xindmap application module.

# `xindmap.app`

To ensure the lifetime of every object used by the application, a single object
is intantiated.
This core has the responsability of initialize other objects such as
controllers, data models, widgets, ...

This module only purpose is to expose core classes for Xindmap.
For now there is only one classe exposed by this module.

## Module exported content

- [`xindmap.app.XindmapApp.XindmapApp`][]
"""

from .XindmapApp import XindmapApp
