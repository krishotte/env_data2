"""Web Routes."""

from masonite.routes import Get, Post

ROUTES = [
    Get('/', 'WelcomeController@show').name('welcome'),

    Post('/envdata', 'DataController@store2'),
    # Post('/envdata2', 'DataController@store2'),

    Get('/envdata/@device_id', 'DataController@show_device_data'),
    Get('/envdata-last', 'DataController@show_last'),
]
