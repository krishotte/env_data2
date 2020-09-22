from orator import DatabaseManager
from dotenv import load_dotenv
from pathlib import Path
from os import environ
from orator import Model
import sys


root_path = Path.cwd().parents[1]
env_path = root_path.joinpath('.env')
load_dotenv(dotenv_path=env_path, verbose=True)

# print(f' environment: {environ}')
sys.path.append(str(root_path))
# from app.Data import Data
# from app.Device import Device

config = {
    'postgres': {
        'driver': 'postgres',
        'host': 'localhost',
        'database': 'env_data_odroid',
        'user': environ['DB_USERNAME'],
        'password': environ['DB_PASSWORD'],
        'prefix': '',
    }
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)


class DataOdroid(Model):
    __table__ = 'env_data'


def get_data_for_import():
    count = DataOdroid.count()
    print(f' {count} datapoints available')

    # all_data = DataOdroid.where('id', '<', 100).order_by('id', 'asc').get()
    all_data = DataOdroid.order_by('id', 'asc').get()
    print(f' selected data: {all_data.count()}')

    return all_data


def import_data(data_to_import):
    print(f' local data count: {Data.count()}')
    device = Device.where('name', '=', 'wired').get()[0]
    print(f' first device: {device.serialize()}')

    for each in data_to_import:
        try:
            device_ = each.device
        except AttributeError:
            device_ = device

        data_ = Data(
            timestamp=each.timestamp,
            battery=each.battery,
            temperature=each.temperature,
            humidity=each.humidity,
            pressure=each.pressure,
        )
        data_.device().associate(device_)
        data_.save()

    print(f' local data count: {Data.count()}')


if __name__ == '__main__':
    data = get_data_for_import()

    from app.Data import Data
    from app.Device import Device

    import_data(data)
