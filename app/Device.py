"""Device Model."""

from config.database import Model


class Device(Model):
    """Device Model."""
    __fillable__ = ['name', 'description']
    __timestamps__ = False
