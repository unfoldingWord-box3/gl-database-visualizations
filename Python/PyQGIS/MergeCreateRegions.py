import processing

# Get the active layer (assuming this script is run within the QGIS Python console)
layer = iface.activeLayer()

# Define the field name (replace 'join_Region' with your desired field name)
field_name = 'join_Region'

# Set the parameters for the dissolve operation
parameters = {
    'INPUT': layer,
    'FIELD': [field_name],
    'SEPARATE_DISJOINT': False,
    'OUTPUT': 'TEMPORARY_OUTPUT'
}

# Run the dissolve operation
result = processing.run("native:dissolve", parameters)

# Check if the dissolve operation was successful
if result['OUTPUT']:
    print("Dissolve operation completed successfully.")
else:
    print("Dissolve operation failed.")
