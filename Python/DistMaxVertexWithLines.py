from qgis.core import QgsField, QgsFeature, QgsGeometry, QgsPointXY, QgsProject, QgsVectorLayer
from qgis.PyQt.QtCore import QVariant
import os

# Replace with the name or path of your point layer
points_layer_name = 'points'

# Replace with the name or path of your polygon layer
polygons_layer_name = 'polygons'

# Replace with the name of the field containing the unique IDs (codes) of polygons in the point layer
overlaps_field_name = 'overlaps'

# Get the point layer
points_layer = QgsProject.instance().mapLayersByName(points_layer_name)[0]

# Get the polygon layer
polygons_layer = QgsProject.instance().mapLayersByName(polygons_layer_name)[0]

# Create a dictionary to store the farthest distances and polygon codes for each point
point_distances = {}

# Create a memory layer for the lines
line_layer = QgsVectorLayer('LineString?crs=' + polygons_layer.crs().toWkt(), 'farthest_distance_lines', 'memory')
line_layer.startEditing()

# Define the field names for the line layer
line_fields = [
    QgsField('point_code', QVariant.String),
    QgsField('polygon_code', QVariant.String),
    QgsField('farthest_distance', QVariant.Double),
]
line_layer.dataProvider().addAttributes(line_fields)
line_layer.updateFields()

# Iterate over the point features
for point_feature in points_layer.getFeatures():
    overlaps = point_feature[overlaps_field_name]
    point_code = point_feature['code']
    point_geometry = point_feature.geometry()

    # Convert overlaps to string and split by comma
    overlaps = str(overlaps)
    polygon_ids = overlaps.split(',')

    for polygon_id in polygon_ids:
        polygon_id = polygon_id.strip()

        # Find the polygon feature based on the ID
        polygon_feature = next((f for f in polygons_layer.getFeatures() if f['code'] == polygon_id), None)

        if polygon_feature:
            polygon_code = polygon_feature['code']
            polygon_geometry = polygon_feature.geometry()
            farthest_distance = 0.0
            farthest_vertex = None

            # Iterate over the polygon vertices
            for vertex in polygon_geometry.vertices():
                distance = point_geometry.distance(QgsGeometry.fromPointXY(QgsPointXY(vertex.x(), vertex.y())))

                if distance > farthest_distance:
                    farthest_distance = distance
                    farthest_vertex = vertex

            # Add the farthest distance and polygon code for the point
            if point_code not in point_distances:
                point_distances[point_code] = []

            point_distances[point_code].append((polygon_code, farthest_distance))

            # Create a line feature from the point to the farthest vertex
            start_point = QgsPointXY(point_geometry.asPoint())
            end_point = QgsPointXY(farthest_vertex.x(), farthest_vertex.y())
            line_geometry = QgsGeometry.fromPolylineXY([start_point, end_point])
            line_feature = QgsFeature(line_layer.fields())
            line_feature.setGeometry(line_geometry)
            line_feature.setAttributes([point_code, polygon_code, farthest_distance])
            line_layer.addFeature(line_feature)

    # Break point to check the progress
    print(f"Processed point with ID: {point_code}")

line_layer.commitChanges()

# Print debug information
print("Farthest Distances:")
for point_code, distances in point_distances.items():
    print(f"Point ID: {point_code}, Distances: {distances}")

# Create a memory layer and add fields
layer_fields = [
    QgsField('point_code', QVariant.String),
    QgsField('farthest_distances', QVariant.String),
    QgsField('polygon_codes', QVariant.String),
]
memory_layer = QgsVectorLayer('Point?crs=' + polygons_layer.crs().toWkt(), 'farthest_distances', 'memory')
memory_layer.dataProvider().addAttributes(layer_fields)
memory_layer.updateFields()

# Add features to the memory layer
features = []
for point_code, distances in point_distances.items():
    feature = QgsFeature()
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(0, 0)))  # Set a dummy geometry
    farthest_distances = [dist[1] for dist in distances]
    polygon_codes = [dist[0] for dist in distances]
    feature.setAttributes([point_code, ','.join(map(str, farthest_distances)), ','.join(polygon_codes)])
    features.append(feature)

memory_layer.dataProvider().addFeatures(features)

# Add the memory layer and line layer to the project
QgsProject.instance().addMapLayer(memory_layer)
QgsProject.instance().addMapLayer(line_layer)

# Break point to check the completion
print('Processing completed successfully.')
