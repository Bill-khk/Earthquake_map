from flask import Flask
import datetime
import pprint
import json

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
    extracted_data = {
        data['id']: {
            'coordinates': data['geometry']['coordinates'],
            'date': datetime.datetime.fromtimestamp(data['properties']['time'] / 1000, datetime.UTC).strftime(
                "%d-%m-%Y"),
            'title': data['properties']['title'],
        }
        for data in response_data['features']
    }

    if response.status_code == 200:
        return extracted_data
    else:
        return response.status_code


retrieved_data = get_EQ_data(start_date, end_date)

pprint.pprint(retrieved_data)  # Method to print dict nicely


# 1.1 Save in JSON file --------------------------------------------------------
def json_saving(data, filename):
    json_object = json.dumps(data)

    with open(f'EQdata/{filename}', "w") as outfile:
        outfile.write(json_object)


# json_saving(retrieved_data, "data.json")

# 1.2 Save in CSV file --------------------------------------------------------

import pandas as pd


def export_data(data, option=1):
    df = pd.DataFrame.from_dict(data, orient='index')  # Index put each dict value as a row
    df = df.reset_index().rename(columns={'index': 'id'})  # And name the key 'id'

    # Convert tuple coordinate into three column and drop the old one
    df[['longitude', 'latitude', 'depth']] = pd.DataFrame(df['coordinates'].tolist(), index=df.index)
    df.drop(columns='coordinates', inplace=True)

    # Save into csv
    if option == 1:
        df.to_csv("EQdata/data.csv", index_label='id', sep=';')
    else:
        df.to_xml("EQdata/data.xml", index=False, root_name="Earthquakes", row_name="Event")


export_data(retrieved_data)

# 2 Creating the Shapefile with Qgis --------------------------------------------------------

import sys
import os
# QGIS_PREFIX_PATH = 'C:/Program Files/QGIS/apps/qgis-ltr'  # Adjust this for your installation
# os.environ['QGIS_PREFIX_PATH'] = QGIS_PREFIX_PATH
# sys.path.append(os.path.join(QGIS_PREFIX_PATH, 'python'))

from qgis.core import QgsApplication, QgsProject, QgsVectorLayer


def Qgis_processing():
    # App initialization
    QGIS_PATH = 'C:/Program Files/QGIS/bin'
    QgsApplication.setPrefixPath(QGIS_PATH, True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    print("QGIS Initialized --------------")

    project = QgsProject.instance()  # App instance initialization
    project.read('geodata/Base.qgz')  # Opening project

    # Loading countries shp file
    uri = "geodata/ne_110m_admin_0_countries.shp"
    vLayer = QgsVectorLayer(uri, "Countries", "ogr")
    QgsProject.instance().addMapLayer(vLayer)
    # project.write()

    # TODO correct URI to make the layer valid in QGIS
    uri = ("file:///C:/Users/billk/OneDrive/Documents/6 - Pycharm Projects/Earthquake_map/EQdata/data.csv"
           "?delimiter=;&xField=longitude&yField=latitude")
    vLayer = QgsVectorLayer(uri, "EQ_data", "delimitedtext")
    QgsProject.instance().addMapLayer(vLayer)
    print('Layers added --------------')
    project.write('geodata/Processing_project.qgs')


Qgis_processing()

# 3 WEBAPP --------------------------------------------------------
# app = Flask(__name__)
# @app.route("/")
# def hello():
#     return "Hello,World!"
# if __name__ == "__main__":
#     app.run()
