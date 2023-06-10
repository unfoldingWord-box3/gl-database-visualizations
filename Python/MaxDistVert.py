from qgis.core import QgsField, QgsFeature, QgsGeometry, QgsPointXY, QgsProject, QgsVectorLayer
from PyQt5.QtCore import QVariant

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
result_layer = QgsVectorLayer('Point?crs=' + repolygons_layer.crs().toWkt(), 'farthest_distances', 'memory')
result_layer.startEditing()

# Add fields to the result layer
result_layer_fields = [
    QgsField('point_iso', QVariant.String),
    QgsField('overlaps', QVariant.String),
    QgsField('farthest_distances', QVariant.String),
    QgsField('farthest_vertices', QVariant.String),
]
result_layer.dataProvider().addAttributes(result_layer_fields)
result_layer.updateFields()

# Iterate over the point features
for point_feature in repoints_layer.getFeatures():
    overlaps = point_feature[overlaps_field_name]
    point_iso = point_feature['iso']
    point_geometry = point_feature.geometry()

    # Convert overlaps to string and split by comma
    overlaps = str(overlaps)
    polygon_ids = overlaps.split(',')

    farthest_distances = []
    farthest_vertices = []

    for polygon_id in polygon_ids:
        polygon_id = polygon_id.strip()

        # Find the polygon feature based on the ID and check if it contains the point
        polygon_feature = next((f for f in repolygons_layer.getFeatures() if f['iso'] == polygon_id), None)

        if polygon_feature and polygon_feature.geometry().contains(point_geometry):
            polygon_iso = polygon_feature['iso']
            polygon_geometry = polygon_feature.geometry()
            farthest_distance = 0.0
            farthest_vertex = None

            # Iterate over the polygon vertices
            for vertex in polygon_geometry.vertices():
                distance = point_geometry.distance(QgsGeometry.fromPointXY(QgsPointXY(vertex.x(), vertex.y())))

                if distance > farthest_distance:
                    farthest_distance = distance
                    farthest_vertex = vertex

            farthest_distances.append(farthest_distance)
            farthest_vertices.append(f"{farthest_vertex.x()},{farthest_vertex.y()}")

    # Create a new feature for the result layer
    result_feature = QgsFeature(result_layer.fields())
    result_feature.setGeometry(point_geometry)
    result_feature.setAttributes([point_iso, overlaps, ','.join(map(str, farthest_distances)), ','.join(farthest_vertices)])
    result_layer.addFeature(result_feature)

result_layer.commitChanges()

# Add the result layer to the project
QgsProject.instance().addMapLayer(result_layer)

# Print debug information
print("Farthest Distances:")
for feature in result_layer.getFeatures():
    point_iso = feature['point_iso']
    overlaps = feature['overlaps']
    farthest_distances = feature['farthest_distances']
    farthest_vertices = feature['farthest_vertices']
    print(f"Point ID: {point_iso}, Overlaps: {overlaps}, Farthest Distances: {farthest_distances}, Farthest Vertices: {farthest_vertices}")

# Print completion message
print('Processing completed successfully.')
