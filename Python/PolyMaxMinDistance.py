import numpy as np
from qgis.core import (QgsVectorLayer, QgsFeature, QgsField, QgsPointXY, QgsGeometry, QgsVectorFileWriter, Qgis)
from qgis.PyQt.QtCore import QVariant

# Assuming layer is your polygon layer
layer = iface.activeLayer()

def get_points_per_unit(area):
    # Adjust these values to fit your needs
    if area < 100:
        return 100
    elif area < 1000:
        return 200
    else:
        return 300

print("Creating a copy of the original layer...")
crs = layer.crs().toWkt()
layer_copy = QgsVectorLayer('Polygon?crs=' + crs, 'layer_copy', 'memory')

print("Starting to edit the copy...")
layer_copy.startEditing()

print("Copying the attributes of the original layer...")
layer_copy_data = layer_copy.dataProvider()
for field in layer.fields():
    layer_copy_data.addAttributes([field])
layer_copy.updateFields()

print("Adding new attributes for the max min distance...")
layer_copy_data.addAttributes([QgsField("MaxMinDistance", QVariant.Double)])
layer_copy.updateFields()

print("Iterating over the original layer...")
for feature in layer.getFeatures():
    polygon = feature.geometry()
    bbox = polygon.boundingBox()

    points_per_unit = get_points_per_unit(polygon.area())
    num_points = int(polygon.area() * points_per_unit)
    points = []

    print(f"Generating points within the bounding box...")
    while not points:
        for _ in range(num_points):
            i = np.random.uniform(bbox.xMinimum(), bbox.xMaximum())
            j = np.random.uniform(bbox.yMinimum(), bbox.yMaximum())
            point = QgsPointXY(i, j)
            geom_point = QgsGeometry.fromPointXY(point)

            if polygon.contains(geom_point): 
                points.append(geom_point)
        if not points:
            print("No points were generated within the polygon. Trying again...")

    max_min_distance = 0

    print("Computing the minimum distance from each point to the polygon...")
    for point in points:
        min_distance = polygon.distance(point)

        if min_distance > max_min_distance:
            max_min_distance = min_distance

    print("Copying the feature from the original layer...")
    new_feature = QgsFeature(layer_copy.fields())
    new_feature.setGeometry(feature.geometry())
    for field in feature.fields():
        try:
            new_feature[field.name()] = feature[field.name()]
        except Exception as e:
            print(f"Error when copying attribute {field.name()}: {str(e)}")

    print("Setting the new attributes...")
    new_feature["MaxMinDistance"] = max_min_distance

    print("Adding the new feature to the copy layer...")
    layer_copy.addFeature(new_feature)

print("Committing the changes and adding the new layer to the map...")
layer_copy.commitChanges()
QgsProject.instance().addMapLayer(layer_copy)

print('New layer with results added to the map.')
