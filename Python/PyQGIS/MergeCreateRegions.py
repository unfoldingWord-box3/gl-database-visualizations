import processing
layer = iface.activeLayer()  # Assuming you are running this script within the QGIS Python console

field_name = 'join_Region'  # Replace 'join_Region' with your desired field name

parameters = {
    'INPUT': layer,
    'FIELD': [field_name],
    'SEPARATE_DISJOINT': False,
    'OUTPUT': 'TEMPORARY_OUTPUT'  # Output set to 'TEMPORARY_OUTPUT' to create a temporary layer
}

result = processing.run("native:dissolve", parameters)

if result['OUTPUT']:
    dissolved_layer = result['OUTPUT']  # Access the temporary layer from the result
    QgsProject.instance().addMapLayer(dissolved_layer)  # Add the temporary layer to the map
    print("Dissolve operation completed successfully. Temporary layer added to the map.")
else:
    print("Dissolve operation failed.")
