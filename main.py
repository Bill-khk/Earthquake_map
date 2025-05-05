from flask import Flask
import datetime

# TODO 1) Get the data from https://earthquake.usgs.gov/fdsnws/event/1/ - Submit on UDEMY
# TODO 2) Create a shapefile from QGIS using PyQGIS - https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/index.html
# TODO 3) Create a webserver that interact with the data and update the display

# 1 API DATA --------------------------------------------------------

import requests

URL_ENDPOINT = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
parameters = {
    'format': 'geojson',
    'starttime': '2014-01-01',
    'endtime': '2014-01-02',
}

response = requests.get(URL_ENDPOINT, params=parameters)
response_data = response.json()
extracted_data = [(data['id'], data['geometry']['coordinates'], data['properties']['time']/1000, data['properties']['title']) for data in response_data['features']]

#extracted_data[2] = datetime.datetime.fromtimestamp(extracted_data[2], datetime.UTC)

if response.status_code == 200:
    for item in extracted_data:
        print(item)




# 3 WEBAPP --------------------------------------------------------
# app = Flask(__name__)
# @app.route("/")
# def hello():
#     return "Hello,World!"
# if __name__ == "__main__":
#     app.run()
