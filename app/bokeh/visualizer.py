# to be run from root directory

from bokeh.plotting import figure, ColumnDataSource, show
from bokeh.models import LinearAxis, Range1d
from pathlib import Path
from dotenv import load_dotenv
import sys
from bokeh.embed import components

root_path = Path.cwd()  # .parents[1]
print(f' root path: {root_path}')
env_path = root_path.joinpath('.env')
load_dotenv(dotenv_path=env_path, verbose=True)

# print(f' environment: {environ}')
sys.path.append(str(root_path))

from app.Device import Device
from app.Data import Data


class Document:
    def __init__(self, device='wired'):
        self.device = Device.where('name', '=', device).get()[0]
        self.graph = figure(x_axis_type='datetime')
        self.graph.sizing_mode = 'stretch_both'
        self.data = ColumnDataSource(data={
            'timestamps': [],
            'temperature': [],
            'humidity': [],
            'pressure': [],
            'battery': [],
        })

    def get_data(self, length=2000):
        db_data = self.device.datas().order_by('id', 'asc').get()
        print(f' acquired {len(db_data)} data points')

        timestamps = []
        temperature = []
        humidity = []
        for data in db_data[-length:]:
            timestamps.append(data.timestamp)
            temperature.append(data.temperature)
            humidity.append(data.humidity)

        print(f' timestamps: {timestamps}')
        print(f' temperature: {temperature}')
        print(f' humidity: {humidity}')

        self.data.data = {
            'timestamps': timestamps,
            'temperature': temperature,
            'humidity': humidity,
        }

    def create_graph(self):

        self.graph.line(
            x='timestamps',
            y='temperature',
            source=self.data,
            color='red',
            y_range_name='temp'
        )
        self.graph.line(
            x='timestamps',
            y='humidity',
            source=self.data,
            color='blue',
            y_range_name='hum'
        )

        hum_max = max(self.data.data['humidity'])
        hum_min = min(self.data.data['humidity'])
        hum_padding = 0.03
        hum_start = hum_min - ((hum_max - hum_min) * hum_padding)
        hum_end = hum_max + ((hum_max - hum_min) * hum_padding)

        temp_max = max(self.data.data['temperature'])
        temp_min = min(self.data.data['temperature'])
        temp_start = temp_min - ((temp_max - temp_min) * hum_padding)
        temp_end = temp_max + ((temp_max - temp_min) * hum_padding)

        self.graph.extra_y_ranges = {
            "hum": Range1d(start=hum_start, end=hum_end),
            "temp": Range1d(start=temp_start, end=temp_end),
        }

        self.graph.yaxis.visible = False
        self.graph.add_layout(LinearAxis(y_range_name='hum', axis_line_color='blue', major_label_text_color='blue'), 'left')
        self.graph.add_layout(LinearAxis(y_range_name='temp', axis_line_color='red', major_label_text_color='red'), 'left')

        # show(self.graph)


def get_graph_components():
    doc = Document()
    doc.get_data(length=4000)
    doc.create_graph()
    script, div = components(doc.graph)

    return script, div


if __name__ == '__main__':
    doc = Document()
    doc.get_data(length=4000)
    doc.create_graph()
    show(doc.graph)
