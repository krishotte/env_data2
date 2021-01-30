"""Web Routes."""

from masonite.routes import Get, Post

ROUTES = [
    Get('/', 'WelcomeController@show').name('welcome'),

    Post('/envdata', 'DataController@store2'),

    # Home route
    Get('/main', 'DataController@show_main'),
    # Data presentation routes
    Get('/envdata/@device_id/@data_length', 'DataController@show_device_data'),
    Get('/envdata-last', 'DataController@show_last'),
    Get('/envdata-stat', 'DataController@show_stat'),

    # Battery
    Get('/battery/@device_id/@data_length', 'DataController@show_batery_data'),

    # API routes
    Get('/api/envdata-last', 'ApiController@show_last'),
    Get('/api/envdata/@device_id/@data_length', 'ApiController@show_device_data')
]
