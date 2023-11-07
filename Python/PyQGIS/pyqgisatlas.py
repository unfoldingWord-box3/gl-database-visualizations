from qgis.core import QgsApplication,QgsProject,QgsLayoutExporter

qgs = QgsApplication([], True)

# load providers
qgs.initQgis()
project = QgsProject.instance()
project.read('geopackage:C:/TEMP/your_project_name.GPKG?projectName=Your_QGIS_Project_Name')

# If you want to see wich layouts are in your project
manager = project.layoutManager()
layouts_list = manager.printLayouts()
for layout in layouts_list:
    print('Layout Name: ',layout.name())

print(layouts_list)

layoutName='Mapa_JPG_2'
layout = manager.layoutByName(layoutName)

myAtlas=layout.atlas()
myAtlas.setFilterFeatures(True)

# If you want to filter your Atlas Selection
myAtlas.setFilterExpression("Your_Field_Name = '%s'" % ('Your_Value'))

# Generate atlas
# It's a QgsLayoutAtlas class 
# https://qgis.org/api/classQgsLayoutAtlas.html#acb3052609fcff21e4f4cf3f9e93780e0

# Starts Layout Generation
myAtlas.beginRender()

# For 0 to Number of features in Atlas Selection
for i in range(0, myAtlas.count()):

    # Creata a exporter Layout for each layout generate with Atlas
    exporter = QgsLayoutExporter(myAtlas.layout())

    print('Saving File: '+str(myAtlas.currentFeatureNumber())+' of '+str(myAtlas.count()))

    # If you want create a PDF's Files
    exporter.exportToPdf('c:/temp/'+myAtlas.currentFilename()+".pdf", QgsLayoutExporter.PdfExportSettings())

    # If you want create a JPG's files
    exporter.exportToImage('c:/temp/'+myAtlas.currentFilename()+".jpg", QgsLayoutExporter.ImageExportSettings())

    # Show wich file is creating
    print('Create File: '+myAtlas.currentFilename())

    # Create Next Layout
    myAtlas.next()

# Close Atlas Creation
myAtlas.endRender()

# Close Qgis
qgs.exitQgis()
Share
Improve this answer
Follow
