def addLegend(layoutName):
#    project = QgsProject.instance()
#    manager = project.layoutManager()
    layout = project.layoutManager().layoutByName(layoutName)
    
    checked_lyrs = [l.name() for l in QgsProject().instance().layerTreeRoot().children() if l.isVisible()]
    checked_lyrs.remove('OpenStreetMap')
    lyrsToRemove = [l for l in project.mapLayers().values() if l.name() not in checked_lyrs]
    legend = QgsLayoutItemLegend(layout)
    #setAutoUpdateModel to false otherwise main layer tree view will also be modified
    legend.setAutoUpdateModel(False)
    root = legend.model().rootGroup()
    for l in lyrsToRemove:
        root.removeLayer(l)
    legend.adjustBoxSize()
    legend.setId('Legend')
    layout.addLayoutItem(legend)
    legend.setFrameEnabled(True)
    legend.setFrameStrokeWidth(QgsLayoutMeasurement(0.3))
    legend.setTitle('Legend')
    legend.attemptMove(QgsLayoutPoint(308, 115, QgsUnitTypes.LayoutMillimeters))
    legend.attemptResize(QgsLayoutSize(104, 40, QgsUnitTypes.LayoutMillimeters))

addLegend('Test Layout')