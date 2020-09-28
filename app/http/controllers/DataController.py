"""A DataController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.response import Response
from masonite.controllers import Controller
import json
from app.Device import Device
from app.Data import Data
from datetime import datetime
from app.bokeh.visualizer import get_graph_components


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

    def show_last(self, view: View):
        try:
            last1 = Device.find(1).datas().order_by('id', 'desc').first()
            last1_serialized = last1.serialize()
            last1_serialized['timestamp'] = last1.serialize()['timestamp'].isoformat()
        except (AttributeError, KeyError):
            last1_serialized = ''

        try:
            last2 = Device.find(2).datas().order_by('id', 'desc').first()
            last2_serialized = last2.serialize()
            last2_serialized['timestamp'] = last2.serialize()['timestamp'].isoformat()
        except (AttributeError, KeyError):
            last2_serialized = ''

        return [last1_serialized, last2_serialized]

    def show_device_data(self, view: View, request: Request, response: Response):
        # print(f' device: {request.param('device_id')})
        # data = Device.find(1).datas().order_by('id', 'asc').get()
        data = Device.find(request.param('device_id')).datas().order_by('id', 'asc').get()
        data = data[-int(request.param('data_length')):]

        data_serialized = data.serialize()

        timestamps = []
        temperature = []
        humidity = []
        for i in range(len(data)):
            data_serialized[i]['timestamp'] = data[i].serialize()['timestamp'].isoformat()
            timestamps.append(data[i].timestamp)
            temperature.append(data[i].temperature)
            humidity.append(data[i].humidity)

        script, div = get_graph_components({
            'timestamps': timestamps,
            'temperature': temperature,
            'humidity': humidity,
        })
        # return response.view('test response')
        # return data_serialized
        return view.render('graph', {
            'div_': div,
            'script_': script,
        })

    def show_main(self, view: View):
        return view.render('main.html')
