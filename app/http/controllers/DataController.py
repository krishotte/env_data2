"""A DataController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.response import Response
from masonite.controllers import Controller
import json
from app.Device import Device
from app.Data import Data
from datetime import datetime


class DataController(Controller):
    """DataController Controller Class."""

    def __init__(self, request: Request):
        """DataController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View):
        pass

    def store(self, request: Request, response: Response):
        data = json.loads(request.input("data"))
        print(f' data: {data}')
        token = request.header('HTTP-X-AUTH-TOKEN')
        print(f' token: {token}')

        device = Device.where('name', '=', data['device']).get()
        print(f' writing device: {device.serialize()}')

        try:
            timestamp = datetime.fromisoformat(data['timestamp'])
        except KeyError:
            timestamp = datetime.utcnow()

        data_point = Data(
            timestamp=timestamp,
            battery=data["battery"],
            temperature=data["temperature"],
            humidity=data["humidity"],
            pressure=data["pressure"]
        )
        data_point.device().associate(device[0])
        data_point.save()
        return response.view('my response')

    def store2(self, request: Request, response: Response):
        # print(f' environment: {request.environ}')
        # print(f' request: {request.all()}')
        # print(f' data header: {request.header("POST_DATA")}')

        data = json.loads(request.header("POST_DATA"))
        print(f' decoded data: {data}')

        try:
            device_name = data['device']
        except KeyError:
            device_name = 'wired'

        device = Device.where('name', '=', device_name).get()
        print(f' writing device: {device.serialize()}')

        try:
            timestamp = datetime.fromisoformat(data['timestamp'])
        except KeyError:
            timestamp = datetime.utcnow()

        data_point = Data(
            timestamp=timestamp,
            battery=data["battery"],
            temperature=data["temperature"],
            humidity=data["humidity"],
            pressure=data["pressure"]
        )
        data_point.device().associate(device[0])
        data_point.save()

        return response.view('done')
