"""Device Model."""

from config.database import Model
from orator.orm import has_many


class Device(Model):
    """Device Model."""
    __fillable__ = ['name', 'description']
    __timestamps__ = False

    @has_many
    def datas(self):
        from app.Data import Data
        return Data
