from flask import Flask
import datetime

# TODO 1) Get the data from https://earthquake.usgs.gov/fdsnws/event/1/ - Submit on UDEMY
# TODO 1.1) Save in a JSON file to be able to work Offline
# TODO 2) Create a shapefile from QGIS using PyQGIS - https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/index.html
# TODO 3) Create a webserver that interact with the data and update the display

# 1 API DATA --------------------------------------------------------
import requests

start_date = '2014-01-01'
end_date = '2014-01-02'


def get_EQ_data(start, end):
    URL_ENDPOINT = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
    parameters = {
        'format': 'geojson',
        'starttime': start,
        'endtime': end,
    }

    response = requests.get(URL_ENDPOINT, params=parameters)
    response_data = response.json()
    extracted_data = [
        (
            data['id'],
            data['geometry']['coordinates'],
            datetime.datetime.fromtimestamp(data['properties']['time'] / 1000, datetime.UTC).strftime("%d-%m-%Y"),
            data['properties']['title']
        )
        for data in response_data['features']
    ]
    if response.status_code == 200:
        return extracted_data
    else:
        return response.status_code


retrieved_data = get_EQ_data(start_date, end_date)
for item in retrieved_data:
    print(item)

# 1.1 Save in JSON file --------------------------------------------------------


# 3 WEBAPP --------------------------------------------------------
# app = Flask(__name__)
# @app.route("/")
# def hello():
#     return "Hello,World!"
# if __name__ == "__main__":
#     app.run()
