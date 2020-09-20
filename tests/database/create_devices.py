# to be run from main directory
import sys
from pathlib import Path
from dotenv import load_dotenv


root_path = Path.cwd()
env_path = root_path.joinpath('.env')
print(f'  root path: {root_path}')
print(f'  env path: {env_path}')

sys.path.append(str(root_path))
load_dotenv(dotenv_path=env_path, verbose=True)

from app.Device import Device


devices = [
    Device(name='wired'),
    Device(name='wireless'),
]

for device in devices:
    device.save()

loaded_devices = Device.order_by('id', 'asc').get()
