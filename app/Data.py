"""Data Model."""

from config.database import Model
from orator.orm import belongs_to


class Data(Model):
    """Data Model."""
    __fillable__ = ['timestamp', 'battery', 'temperature', 'humidity', 'pressure']
    __timestamps__ = False

    @belongs_to
    def device(self):
        from app.Device import Device
        return Device
