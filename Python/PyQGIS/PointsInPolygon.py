polygon_layer = QgsProject.instance().mapLayersByName('polygon_layer')[0]
point_layer = QgsProject.instance().mapLayersByName('point_layer')[0]

# Create the output layer
output_layer = QgsVectorLayer('Polygon?crs='+ polygon_layer.crs().toWkt(), 'output_layer' , 'memory')
provider = output_layer.dataProvider()

fields = polygon_layer.pendingFields()
fields.append(QgsField('POINT_COUNT', QVariant.Int, '', 10, 0))
provider.addAttributes(fields)

# Create spatial index
point_index = QgsSpatialIndex()
for point_feature in point_layer.getFeatures():
    point_index.insertFeature(point_feature)

# Loop over each polygon feature
for polygon_feature in polygon_layer.getFeatures():
    polygon_attributes = polygon_feature.attributes()
    polygon_geometry = polygon_feature.geometry()
    geometry_engine = QgsGeometry.createGeometryEngine(polygon_geometry.geometry())
    geometry_engine.prepareGeometry()
    intersecting_point_ids = point_index.intersects(polygon_geometry.boundingBox())
    point_count = 0
    if len(intersecting_point_ids) > 0:
        point_request = QgsFeatureRequest().setFilterFids(intersecting_point_ids)
        for point_feature in point_layer.getFeatures(point_request):
            point_geometry = point_feature.geometry()
            if point_geometry.within(polygon_geometry):
                point_count += 1
    output_feature = QgsFeature()
    output_feature.setGeometry(polygon_geometry)
    output_feature.setAttributes(polygon_attributes)
    output_feature.setAttribute('POINT_COUNT', point_count)
    provider.addFeatures([output_feature])

# Add the layer to the map
QgsProject.instance().addMapLayer(output_layer)