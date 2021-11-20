"""
Version: v.01 
Name : DV_OL_CT_OLB
Group : 

"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Dv_gl_ol_voronoi_smoothening(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('InputData', 'Input Data', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('InputData (2)', 'Base Map', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('FieldwithUniqueValues', 'Field with Unique Values', type=QgsProcessingParameterField.Any, parentLayerParameterName='InputData', allowMultiple=False, defaultValue=''))
        self.addParameter(QgsProcessingParameterNumber('VerticestoAdd', 'Vertices to Add', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=100, defaultValue=5))
        self.addParameter(QgsProcessingParameterNumber('Tolerance', 'Tolerance', type=QgsProcessingParameterNumber.Double, minValue=-1.79769e+308, maxValue=1.79769e+308, defaultValue=0.05))
        self.addParameter(QgsProcessingParameterFeatureSink('Gl_ol_voronoi', 'GL_OL_Voronoi', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(12, model_feedback)
        results = {}
        outputs = {}

        # OL_Country filter
        # Edit the filter by Country
        alg_params = {
            'INPUT': parameters['InputData'],
            'OUTPUT_Data': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ol_countryFilter'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Map_filter
        # Edit the Map by Country
        alg_params = {
            'INPUT': parameters['InputData (2)'],
            'OUTPUT_Data': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Map_filter'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Voronoi
        alg_params = {
            '-l': False,
            '-t': False,
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,  # auto
            'GRASS_REGION_PARAMETER': outputs['Map_filter']['OUTPUT_Data'],
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'input': outputs['Ol_countryFilter']['OUTPUT_Data'],
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Voronoi'] = processing.run('grass7:v.voronoi', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Clip
        alg_params = {
            'INPUT': outputs['Voronoi']['output'],
            'OVERLAY': outputs['Map_filter']['OUTPUT_Data'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Densify by count
        alg_params = {
            'INPUT': outputs['Clip']['OUTPUT'],
            'VERTICES': parameters['VerticestoAdd'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DensifyByCount'] = processing.run('native:densifygeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Extract vertices
        alg_params = {
            'INPUT': outputs['DensifyByCount']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractVertices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Geometry by expression
        alg_params = {
            'EXPRESSION': 'make_point($x +randf( -@Tolerance ,@Tolerance), $y + randf( -@Tolerance ,@Tolerance))',
            'INPUT': outputs['ExtractVertices']['OUTPUT'],
            'OUTPUT_GEOMETRY': 2,  # Point
            'WITH_M': False,
            'WITH_Z': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GeometryByExpression'] = processing.run('native:geometrybyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Points to path
        alg_params = {
            'CLOSE_PATH': True,
            'DATE_FORMAT': '',
            'GROUP_FIELD': parameters['FieldwithUniqueValues'],
            'INPUT': outputs['GeometryByExpression']['OUTPUT'],
            'ORDER_FIELD': 'vertex_index',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PointsToPath'] = processing.run('qgis:pointstopath', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Lines to polygons
        alg_params = {
            'INPUT': outputs['PointsToPath']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LinesToPolygons'] = processing.run('qgis:linestopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': parameters['Tolerance'],
            'END_CAP_STYLE': 0,  # Round
            'INPUT': outputs['LinesToPolygons']['OUTPUT'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Clip
        alg_params = {
            'INPUT': outputs['Buffer']['OUTPUT'],
            'OVERLAY': outputs['Map_filter']['OUTPUT_Data'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': parameters['FieldwithUniqueValues'],
            'FIELDS_TO_COPY': [''],
            'FIELD_2': parameters['FieldwithUniqueValues'],
            'INPUT': outputs['Clip']['OUTPUT'],
            'INPUT_2': parameters['InputData'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'OUTPUT': parameters['Gl_ol_voronoi']
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Gl_ol_voronoi'] = outputs['JoinAttributesByFieldValue']['OUTPUT']
        return results

    def name(self):
        return 'DV_GL_OL_Voronoi_Smoothening'

    def displayName(self):
        return 'DV_GL_OL_Voronoi_Smoothening'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Dv_gl_ol_voronoi_smoothening()
