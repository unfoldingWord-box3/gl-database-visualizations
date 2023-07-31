import os
import json
import csv
from qgis.core import (
    QgsVectorLayer, QgsVectorFileWriter, QgsField, QgsProject, QgsFeature
)
from qgis.PyQt.QtCore import QVariant

# Providing paths for the data inputs
base_path = "D:/SEVENX/DATA_SET/2023/July/Output_folder"
input_gpkg_path = os.path.join(base_path, "world.gpkg")
output_folder = os.path.join(base_path, "GeoJSON_Files")
output_csv_path = os.path.join(base_path, "output.csv")

# Loading the input data
input_gpkg = QgsVectorLayer(input_gpkg_path, 'Input GPKG', 'ogr')
if not input_gpkg.isValid():
    print('Failed to load input GPKG')
    exit(1)

# Add the input layer to the map canvas for visualization (optional)
QgsProject.instance().addMapLayer(input_gpkg)

# Creating the output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Add a new field to the original layer to store GeoJSON strings
input_gpkg.dataProvider().addAttributes([QgsField("geojson", QVariant.String)])
input_gpkg.updateFields()
geojson_field_index = input_gpkg.fields().indexOf("geojson")

# Loop through each feature and export to separate GeoJSON files
for feature in input_gpkg.getFeatures():
    # Create a new vector layer for each feature
    feature_layer = QgsVectorLayer("Polygon?crs=epsg:4326", "Feature", "memory")
    feature_layer.startEditing()
    feature_layer.addFeature(feature)
    feature_layer.commitChanges()

    # Generate the output file path using original feature's name
    output_file = os.path.join(output_folder, f"{feature['NAME']}.geojson")

    # Export the feature layer to GeoJSON
    QgsVectorFileWriter.writeAsVectorFormat(feature_layer, output_file, "utf-8", feature_layer.crs(), "GeoJSON")

    # Read the GeoJSON file into a Python object
    with open(output_file, 'r') as f:
        geojson_data = json.load(f)
    # Remove the 'crs' property if it exists
    geojson_data.pop('crs', None)

    # Write the GeoJSON string of the feature (without 'crs') to the new field in the original layer
    geojson_string = json.dumps(geojson_data)
    input_gpkg.startEditing()
    input_gpkg.changeAttributeValue(feature.id(), geojson_field_index, geojson_string)
    input_gpkg.commitChanges()

    # Remove the temporary feature layer
    QgsProject.instance().removeMapLayer(feature_layer.id())

# Prepare the CSV file
with open(output_csv_path, 'w', newline='') as csvfile:
    fieldnames = [field.name() for field in input_gpkg.fields()]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each feature and write to CSV
    for feature in input_gpkg.getFeatures():
        # Prepare feature attributes as a dictionary
        attributes_dict = {field.name(): feature[field.name()] for field in input_gpkg.fields()}
        
        # Write feature to CSV
        writer.writerow(attributes_dict)

print("Export complete")
