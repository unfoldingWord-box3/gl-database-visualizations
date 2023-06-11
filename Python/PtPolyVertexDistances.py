from qgis.core import QgsField, QgsFeature, QgsGeometry, QgsPointXY, QgsProject, QgsVectorLayer, QgsVectorFileWriter
from PyQt5.QtCore import QVariant
import datetime
import os


# Replace with the name or path of your point layer
repoints_layer_name = 'repoints'

# Replace with the name or path of your polygon layer
repolygons_layer_name = 'repolygons'

# Replace with the name of the field containing the unique IDs (isos) of repolygons in the point layer
overlaps_field_name = 'overlaps'

# Get the point layer
repoints_layer = QgsProject.instance().mapLayersByName(repoints_layer_name)[0]

# Get the polygon layer
repolygons_layer = QgsProject.instance().mapLayersByName(repolygons_layer_name)[0]

# Create a new memory layer for the results
result_layer = QgsVectorLayer('Point?crs=' + repolygons_layer.crs().toWkt(), 'vertexdistances', 'memory')
result_layer.startEditing()

# Add fields to the result layer
result_layer_fields = [
    QgsField('point_iso', QVariant.String, 'Point ISO'),
    QgsField('overlaps', QVariant.String, 'Overlapping Polygons'),
    QgsField('num_overlaps', QVariant.Int, 'Number of Overlapping Polygons'),
    QgsField('farthest_distances', QVariant.String, 'Farthest Distances (km)'),
    QgsField('nearest_distances', QVariant.String, 'Nearest Distances (km)'),
    QgsField('num_distances', QVariant.Int, 'Number of Distances'),
    QgsField('all_distances_calculated', QVariant.Bool, 'All Distances Calculated'),
]
result_layer.dataProvider().addAttributes(result_layer_fields)
result_layer.updateFields()

# Create an index for the 'all_distances_calculated' field
result_layer.dataProvider().createSpatialIndex()

# Iterate over the point features
for point_feature in repoints_layer.getFeatures():
    overlaps = point_feature[overlaps_field_name]
    point_iso = point_feature['iso']
    point_geometry = point_feature.geometry()

    # Convert overlaps to string and split by comma
    overlaps = str(overlaps)
    polygon_ids = overlaps.split(',')

    farthest_distances = []
    nearest_distances = []

    for polygon_id in polygon_ids:
        polygon_id = polygon_id.strip()

        # Find the polygon feature based on the ID
        polygon_features = repolygons_layer.getFeatures(QgsFeatureRequest().setFilterExpression('iso = ' + "'" + polygon_id + "'"))

        if not polygon_features:
            print(f"No polygon found with ID: {polygon_id}")
            continue

        for polygon_feature in polygon_features:
            polygon_iso = polygon_feature['iso']
            polygon_geometry = polygon_feature.geometry()

            farthest_distance = 0.0
            nearest_distance = float('inf')

            # Iterate over the polygon vertices
            for vertex in polygon_geometry.vertices():
                distance = point_geometry.distance(QgsGeometry.fromPointXY(QgsPointXY(vertex.x(), vertex.y()))) / 1000.0

                if distance > farthest_distance:
                    farthest_distance = distance

                if distance < nearest_distance:
                    nearest_distance = distance

            farthest_distances.append(farthest_distance)
            nearest_distances.append(nearest_distance)

    # Check if the number of distances matches the number of overlaps
    all_distances_calculated = len(farthest_distances) == len(polygon_ids)

    # Create a new feature for the result layer
    result_feature = QgsFeature(result_layer.fields())
    result_feature.setGeometry(point_geometry)
    result_feature.setAttributes([
        point_iso,
        overlaps,
        len(polygon_ids),
        ','.join(map(str, farthest_distances)),
        ','.join(map(str, nearest_distances)),
        len(farthest_distances),
        all_distances_calculated,
    ])
    result_layer.addFeature(result_feature)

result_layer.commitChanges()

# Export the result layer to a CSV file
project_path = QgsProject.instance().homePath()
output_csv_path = os.path.join(project_path, 'vertexdistances.csv')
QgsVectorFileWriter.writeAsVectorFormat(result_layer, output_csv_path, 'utf-8', result_layer.crs(), 'CSV')

# Add the result layer to the project
QgsProject.instance().addMapLayer(result_layer)

# Print completion message
print('Processing completed successfully.')
