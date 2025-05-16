from flask import Flask
import datetime
import pprint
import json
import math
import requests
import pandas as pd


# 1) Get the data from https://earthquake.usgs.gov/fdsnws/event/1/ - Submit on UDEMY
# 1.1) Save in a JSON file to be able to work Offline
# TODO 2) Create a shapefile from QGIS using PyQGIS - https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/index.html
# TODO 3) Create a webserver that interact with the data and update the display

# 1 API DATA --------------------------------------------------------

start_date = '2014-01-01'
end_date = '2014-01-02'


def felt_radius(M, D):  # With M the magnitude and D the depth in KM
    euler = 2.718
    radius = 10 ** (0.43 * M) * math.exp(-0.005 * D) # TODO Are the unit correct ? Check with the projection
    # Bakun & Wentworth, 1997 - Bulletin of the Seismological Society of America
    return radius


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
            'mag': data['properties']['mag'],
            'felt_radius': round(felt_radius(data['properties']['mag'], data['geometry']['coordinates'][2]), 2),
        }
        for data in response_data['features']
    }

    if response.status_code == 200:
        return extracted_data
    else:
        return response.status_code


# 1.1 Save in JSON file --------------------------------------------------------
def json_saving(data, filename):
    json_object = json.dumps(data)

    with open(f'EQdata/{filename}', "w") as outfile:
        outfile.write(json_object)


# json_saving(retrieved_data, "data.json")

# 1.2 Save in CSV file --------------------------------------------------------

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


# 2 Creating the Shapefile with Qgis --------------------------------------------------------

from qgis.core import (
    QgsApplication, QgsProject, QgsVectorLayer, QgsProcessingFeedback
)
from qgis.analysis import QgsNativeAlgorithms
import qgis.processing
import processing  # ✅ This is enough to load the processing plugin


def Qgis_processing():
    # QGIS prefix and init
    QGIS_PREFIX_PATH = "C:/OSGeo4W/apps/qgis-ltr"
    QgsApplication.setPrefixPath(QGIS_PREFIX_PATH, True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    print("QGIS Initialized --------------")

    # ✅ Register the native algorithms ONLY
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    project = QgsProject.instance()
    project.read('geodata/Base.qgz')

    # Load base layer
    uri = "geodata/ne_110m_admin_0_countries.shp"
    vLayer = QgsVectorLayer(uri, "Countries", "ogr")
    QgsProject.instance().addMapLayer(vLayer)

    # Load EQ CSV layer
    uri = ("file:///C:/Users/billk/OneDrive/Documents/6 - Pycharm Projects/Earthquake_map/EQdata/data.csv"
           "?delimiter=;&xField=longitude&yField=latitude")
    eqLayer = QgsVectorLayer(uri, "EQ_data", "delimitedtext")  # Create the layer
    eqLayer = QgsProject.instance().addMapLayer(eqLayer)  # Add the layer
    print('Layers added --------------')

    # Buffer parameters
    params = {
        'INPUT': eqLayer,
        'DISTANCE': 0,
        'DYNAMIC': True,  # This enables field-based buffer distances
        'DISTANCE_FIELD_NAME': 'felt_radius',
        'OUTPUT': "C:/Users/billk/OneDrive/Documents/6 - Pycharm Projects/Earthquake_map/geodata/layer_output/EQbuffer.shp",
    }

    feedback = QgsProcessingFeedback()
    buffer_process = qgis.processing.run("native:buffer", params, feedback=feedback)
    buffer_path = buffer_process['OUTPUT']
    buffer_layer = QgsVectorLayer(buffer_path, "EQ_Buffer", "ogr")

    if buffer_layer.isValid():
        QgsProject.instance().addMapLayer(buffer_layer)
        print("Buffer layer added and saved.")
    else:
        print("Buffer layer failed to load.")

    project.write('geodata/Processing_project.qgs')
    qgs.exitQgis()

# 3 WEBAPP --------------------------------------------------------
# app = Flask(__name__)
# @app.route("/")
# def hello():
#     return "Hello,World!"
# if __name__ == "__main__":
#     app.run()


# MAIN -------------------------------------------

retrieved_data = get_EQ_data(start_date, end_date)  # Get data from API
pprint.pprint(retrieved_data)  # Method to print dict nicely
export_data(retrieved_data)  # Export to CSV
#TODO Check the unit and projection of the imported DATA
#Qgis_processing()  # Initiate QGIS and import data
