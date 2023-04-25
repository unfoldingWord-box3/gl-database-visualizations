import os

# Define file paths to data
base_path = "/Users/researchuser/data"
polygon_path = os.path.join(base_path, "stl.gpkg")
points_path = os.path.join(base_path, "pts.gpkg")
stats_path = os.path.join(base_path, "Stats.gpkg")
output_path = os.path.join(base_path, "output.gpkg")

# Load the lng polygon layer
layer1 = QgsVectorLayer(polygon_path, "polygon", "ogr")

if not layer1.isValid():
    print("Layer 1 failed to load!")

# Load the lng points layer
layer2 = QgsVectorLayer(points_path, "points", "ogr")

if not layer2.isValid():
    print("Layer 2 failed to load!")

# Add both layers to the map canvas
QgsProject.instance().addMapLayer(layer1)
QgsProject.instance().addMapLayer(layer2)

# Start editing and add the field to the layer
layer2.startEditing()
field_name = 'poly_boundary'

if not layer2.fields().indexFromName(field_name) >= 0:
    layer2.addAttribute(QgsField(field_name, QVariant.String))

# Define the expression
expression = QgsExpression("aggregate('polygon', aggregate:='concatenate', expression:=\"iso\", concatenator:=',', filter:=intersects($geometry, geometry(@parent)))")

# Create an expression context
context = QgsExpressionContext()

# Loop through the point layer features and set the value of the new field
for feature in layer2.getFeatures():
    context.setFeature(feature)  # Set the feature scope in the expression context
    value = expression.evaluate(context)  # Evaluate the expression for the current feature
    feature.setAttribute(feature.fieldNameIndex(field_name), value)  # Set the value of the new field
    layer2.updateFeature(feature)  # Update the feature in the layer

layer2.commitChanges()

# Perform statistics by category
results = processing.runAndLoadResults("qgis:statisticsbycategories",
                                       {'INPUT': points_path,
                                        'VALUES_FIELD_NAME': 'fid',
                                        'CATEGORIES_FIELD_NAME': ['poly_boundary'],
                                        'OUTPUT': stats_path})

QgsApplication.processEvents()  # Wait for the previous process to finish before running the next one

# Dropping the unnecessary fields
results1 = processing.runAndLoadResults("native:deletecolumn",
                                        {'INPUT': stats_path,
                                         'COLUMN': ['fid', 'unique', 'min', 'max', 'range', 'sum', 'mean', 'median', 'stddev', 'minority', 'majority', 'q1', 'q3', 'iqr'],
                                         'OUTPUT': output_path})

# Print field names in layer1
for field in layer1.fields():
    print(field.name())

# Print poly_boundary values for features in layer2
for feature in layer2.getFeatures():
    print(feature["poly_boundary"])
