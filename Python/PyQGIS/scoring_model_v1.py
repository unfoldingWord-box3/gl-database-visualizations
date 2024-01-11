"""
Model exported as python.
Name : complete_scoring_01_11_2023
Group : 
With QGIS : 32812
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
import processing


class Complete_scoring_01_11_2023(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('minor_lang', 'minor_Lang', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        # no filter. all 208
        self.addParameter(QgsProcessingParameterVectorLayer('both_ab_lng', 'both_ab_lng', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        # "iso" IN ('aar', 'abs', 'ace', 'acm', 'acq', 'acw', 'aeb', 'afb', 'afr', 'ajp', 'aka', 'aln', 'als', 'apc', 'apd', 'arq', 'ars', 'ary', 'arz', 'asm', 'ayl', 'aym', 'ayn', 'aze', 'bal', 'bam', 'ban', 'bej', 'bem', 'ben', 'bho', 'bjn', 'bod', 'brh', 'bug', 'cat', 'ceb', 'cjk', 'cjy', 'cmn', 'deu', 'dgo', 'din', 'dje', 'dzo', 'emk', 'ewe', 'fan', 'fon', 'fuc', 'fuf', 'ful', 'fuv', 'fvr', 'gan', 'grn', 'guj', 'hak', 'hau', 'hil', 'hin', 'hsn', 'ibo', 'ilo', 'ita', 'jav', 'kan', 'kas', 'kau', 'kaz', 'kbp', 'kik', 'kor', 'kpe', 'ktu', 'kua', 'kur', 'lao', 'lbj', 'lin', 'lua', 'lug', 'luo', 'mad', 'mai', 'mak', 'mal', 'mar', 'men', 'mey', 'min', 'mni', 'mnk', 'mon', 'mos', 'msa', 'nag', 'naq', 'nde', 'nep', 'nya', 'orm', 'ory', 'pan', 'pcm', 'pes', 'pga', 'pmy', 'pnb', 'prs', 'pus', 'que', 'raj', 'sag', 'sba', 'scl', 'scn', 'ses', 'shu', 'skr', 'sna', 'snd', 'snk', 'som', 'sot', 'ssw', 'sun', 'sus', 'swa', 'tam', 'tel', 'tem', 'tet', 'tgk', 'tir', 'tmh', 'tsn', 'tso', 'tuk', 'uig', 'umb', 'urd', 'uzb', 'vmw', 'wol', 'wti', 'wuu', 'xho', 'yor', 'yue', 'zha', 'zul')
        self.addParameter(QgsProcessingParameterVectorLayer('type_a_lng', 'type_a_lng', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        # "iso" NOT IN ('aar', 'abs', 'ace', 'acm', 'acq', 'acw', 'aeb', 'afb', 'afr', 'ajp', 'aka', 'aln', 'als', 'apc', 'apd', 'arq', 'ars', 'ary', 'arz', 'asm', 'ayl', 'aym', 'ayn', 'aze', 'bal', 'bam', 'ban', 'bej', 'bem', 'ben', 'bho', 'bjn', 'bod', 'brh', 'bug', 'cat', 'ceb', 'cjk', 'cjy', 'cmn', 'deu', 'dgo', 'din', 'dje', 'dzo', 'emk', 'ewe', 'fan', 'fon', 'fuc', 'fuf', 'ful', 'fuv', 'fvr', 'gan', 'grn', 'guj', 'hak', 'hau', 'hil', 'hin', 'hsn', 'ibo', 'ilo', 'ita', 'jav', 'kan', 'kas', 'kau', 'kaz', 'kbp', 'kik', 'kor', 'kpe', 'ktu', 'kua', 'kur', 'lao', 'lbj', 'lin', 'lua', 'lug', 'luo', 'mad', 'mai', 'mak', 'mal', 'mar', 'men', 'mey', 'min', 'mni', 'mnk', 'mon', 'mos', 'msa', 'nag', 'naq', 'nde', 'nep', 'nya', 'orm', 'ory', 'pan', 'pcm', 'pes', 'pga', 'pmy', 'pnb', 'prs', 'pus', 'que', 'raj', 'sag', 'sba', 'scl', 'scn', 'ses', 'shu', 'skr', 'sna', 'snd', 'snk', 'som', 'sot', 'ssw', 'sun', 'sus', 'swa', 'tam', 'tel', 'tem', 'tet', 'tgk', 'tir', 'tmh', 'tsn', 'tso', 'tuk', 'uig', 'umb', 'urd', 'uzb', 'vmw', 'wol', 'wti', 'wuu', 'xho', 'yor', 'yue', 'zha', 'zul')
        self.addParameter(QgsProcessingParameterVectorLayer('type_b_lng', 'type_b_lng', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output', 'output', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(18, model_feedback)
        results = {}
        outputs = {}

        # repro_maj_lng
        alg_params = {
            'INPUT': parameters['type_a_lng'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7755'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Repro_maj_lng'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # both_ab_overlaps
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'both_ab_overlaps',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'array_to_string(overlay_intersects(\r\nlayer:=     @both_ab_lng ,\r\nexpression:=major_lng_iso\r\n))',
            'INPUT': parameters['minor_lang'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Both_ab_overlaps'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # overlaps_type_a
        alg_params = {
            'FIELD_LENGTH': 500,
            'FIELD_NAME': 'overlaps_type_a',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'array_to_string(overlay_intersects(\r\nlayer:= @type_a_lng ,\r\nexpression:=major_lng_iso\r\n))',
            'INPUT': outputs['Both_ab_overlaps']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Overlaps_type_a'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': outputs['Repro_maj_lng']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # overlaps_type_b
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'overlaps_type_b',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'array_to_string(overlay_intersects(\r\nlayer:=  @type_b_lng ,\r\nexpression:=major_lng_iso\r\n))',
            'INPUT': outputs['Overlaps_type_a']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Overlaps_type_b'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # repro_maj_lng_lines
        alg_params = {
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Repro_maj_lng_lines'] = processing.run('native:polygonstolines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # repro_min_lng
        alg_params = {
            'INPUT': outputs['Overlaps_type_b']['OUTPUT'],
            'OPERATION': '',
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:7755'),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Repro_min_lng'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # max_min(D)
        alg_params = {
            'FIELD_LENGTH': 500,
            'FIELD_NAME': 'D',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'array_to_string(\r\n    array_foreach(\r\n        string_to_array("overlaps_type_a"),\r\n        round(\r\n            distance(\r\n                $geometry, \r\n                boundary(\r\n                    minimal_circle(\r\n                        geometry(\r\n                            get_feature( @repro_maj_lng_OUTPUT , \'iso\', @element)\r\n                        )\r\n                    )\r\n                )\r\n            ) / 1000\r\n        )\r\n    )\r\n)\r\n',
            'INPUT': outputs['Repro_min_lng']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Max_mind'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # min(b)
        alg_params = {
            'FIELD_LENGTH': 500,
            'FIELD_NAME': 'b',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'array_to_string(\r\n    array_foreach(\r\n        string_to_array("overlaps_type_a", \',\'),\r\n        round(to_string(distance($geometry, geometry(get_feature( @repro_maj_lng_lines_OUTPUT , \'iso\', @element))))/1000\r\n    )\r\n))',
            'INPUT': outputs['Max_mind']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Minb'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # D-b
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'D-b',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'array_to_string(\r\n    array_foreach(\r\n        string_to_array("D"),\r\n        to_real(@element) - to_real(array_get(string_to_array("b"), array_find(string_to_array("D"), @element)))\r\n    )\r\n)\r\n',
            'INPUT': outputs['Minb']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Db'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # fx(a)
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'fxa',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'array_to_string(\r\n    array_foreach(\r\n        generate_series(0, array_length(string_to_array("D-b")) - 1),\r\n        21.6679 * ln(101 - 100 * (to_real(array_get(string_to_array("D-b"), @element)) / to_real(array_get(string_to_array("D"), @element))))\r\n    )\r\n)\r\n',
            'INPUT': outputs['Db']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Fxa'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # lngb1
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'lngb1',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'string_to_array("Overlaps_type_b")[0]',
            'INPUT': outputs['Fxa']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Lngb1'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # lngb2
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'lngb2',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'string_to_array("Overlaps_type_b")[1]',
            'INPUT': outputs['Lngb1']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Lngb2'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # lngb3
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'lngb3',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'string_to_array("Overlaps_type_b")[2]',
            'INPUT': outputs['Lngb2']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Lngb3'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # fx_lngb1
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'fx_lngb1',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'aggregate(\r\n    layer:=\'Danny_score_e1e6d035_60c8_4fb7_9c0a_da935ec21eea\',\r\n    aggregate:=\'concatenate\',\r\n    expression:="confidenceB",\r\n    filter:=("country" = attribute(@parent,\'country\')AND "code" = attribute(@parent,\'lngb1\'))\r\n)',
            'INPUT': outputs['Lngb3']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Fx_lngb1'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # fx_lngb2
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'fx_lngb2',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'aggregate(\r\n    layer:=\'Danny_score_e1e6d035_60c8_4fb7_9c0a_da935ec21eea\',\r\n    aggregate:=\'concatenate\',\r\n    expression:="confidenceB",\r\n    filter:=("country" = attribute(@parent,\'country\')AND "code" = attribute(@parent,\'lngb2\'))\r\n)',
            'INPUT': outputs['Fx_lngb1']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Fx_lngb2'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # fx_lngb3
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'fx_lngb3',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'aggregate(\r\n    layer:=\'Danny_score_e1e6d035_60c8_4fb7_9c0a_da935ec21eea\',\r\n    aggregate:=\'concatenate\',\r\n    expression:="confidenceB",\r\n    filter:=("country" = attribute(@parent,\'country\')AND "code" = attribute(@parent,\'lngb3\'))\r\n)',
            'INPUT': outputs['Fx_lngb2']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Fx_lngb3'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # fxb
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'fxb',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'regexp_replace(\n concat(\n if("fx_lngb1" is not null, "fx_lngb1", \'\'), \',\',\n if("fx_lngb2" is not null, "fx_lngb2", \'\'), \',\',\n "fx_lngb3"\n ),\n \'[,\\\\s]*$\', \'\'\n)\n',
            'INPUT': outputs['Fx_lngb3']['OUTPUT'],
            'OUTPUT': parameters['Output']
        }
        outputs['Fxb'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output'] = outputs['Fxb']['OUTPUT']
        return results

    def name(self):
        return 'complete_scoring_01_11_2023'

    def displayName(self):
        return 'complete_scoring_01_11_2023'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Complete_scoring_01_11_2023()
