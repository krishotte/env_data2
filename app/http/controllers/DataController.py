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
        device_id = request.param('device_id')
        data_length = int(request.param('data_length'))
        data = Device.find(device_id).datas().order_by('id', 'desc').take(data_length).get()

        timestamps = [point.timestamp for point in data]
        temperature = [point.temperature for point in data]
        humidity = [point.humidity for point in data]

        script, div = get_graph_components({
            'timestamps': timestamps,
            'temperature': temperature,
            'humidity': humidity,
        })

        return view.render('graph', {
            'div_': div,
            'script_': script,
        })

    def show_batery_data(self, request: Request, view: View):
        device_id = request.param('device_id')
        data_length = int(request.param('data_length'))
        data = Device.find(device_id).datas().order_by('id', 'desc').take(data_length).get()

        timestamps = [point.timestamp for point in data]
        temperature = [point.battery for point in data]

        print(f' timestamps: {timestamps}')
        print(f' battery: {temperature}')

        script, div = get_graph_components({
            'timestamps': timestamps,
            'temperature': temperature,
            'humidity': temperature,
        })

        return view.render('graph', {
            'div_': div,
            'script_': script,
        })

    def show_main(self, view: View):
        return view.render('main.html')

    def show_stat(self, view: View, response: Response):
        devices = Device.all()
        stats = []
        last_data = []
        for device in devices:
            stats.append(
                {
                    'count': Device.find(device.id).datas().count()
                }
            )
            last_data.append(
                device.datas().order_by('id', 'desc').first().serialize()
            )
        print(f' stats: {stats}')
        print(f' last data: {last_data}')
        return view.render('stats', {
            'devices': devices,
            'stats': stats,
            'last': last_data,
        })
