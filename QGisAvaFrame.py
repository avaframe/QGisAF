# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSink)
from qgis import processing
import avaframe
from avaframe.in3Utils import initializeProject as iP


class AvaFrameQGis(QgsProcessingAlgorithm):

    DEM = 'DEM'
    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return AvaFrameQGis()

    def name(self):
        return 'avaframeqgis'

    def displayName(self):
        return self.tr('AvaFrame QGis')

    def group(self):
        return self.tr('AvaFrame')

    def groupId(self):
        return 'avaframe'

    def shortHelpString(self):
        """
        AvaFrame QGis starter
        """
        return self.tr("AvaFrame QGis script")

    def initAlgorithm(self, config=None):

        print('In init')
        # self.addParameter(QgsProcessingParameterRasterLayer(
        #     self.DEM,
        #     self.tr("DEM layer")))

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        # self.addParameter(
        #     QgsProcessingParameterFeatureSink(
        #         self.OUTPUT,
        #         self.tr('Output layer')
        #     )
        # )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        # source = self.parameterAsSource(
        #     parameters,
        #     self.INPUT,
        #     context
        # )

        # # If source was not found, throw an exception to indicate that the algorithm
        # # encountered a fatal error. The exception text can be any string, but in this
        # # case we use the pre-built invalidSourceError method to return a standard
        # # helper text for when a source cannot be evaluated
        # if source is None:
        #     raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        iP.initializeFolderStruct('/home/felix/tmp/TestAva2')
        dest_id = 0
        feedback.pushInfo('Hallo')
        # (sink, dest_id) = self.parameterAsSink(
        #     parameters,
        #     self.OUTPUT,
        #     context,
        #     source.fields(),
        #     source.wkbType(),
        #     source.sourceCrs()
        # )

        # # Send some information to the user
        # feedback.pushInfo('CRS is {}'.format(source.sourceCrs().authid()))

        # # If sink was not created, throw an exception to indicate that the algorithm
        # # encountered a fatal error. The exception text can be any string, but in this
        # # case we use the pre-built invalidSinkError method to return a standard
        # # helper text for when a sink cannot be evaluated
        # if sink is None:
        #     raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        # # Compute the number of steps to display within the progress bar and
        # # get features from source
        # total = 100.0 / source.featureCount() if source.featureCount() else 0
        # features = source.getFeatures()

        # for current, feature in enumerate(features):
        #     # Stop the algorithm if cancel button has been clicked
        #     if feedback.isCanceled():
        #         break

        #     # Add a feature in the sink
        #     sink.addFeature(feature, QgsFeatureSink.FastInsert)

        #     # Update the progress bar
        #     feedback.setProgress(int(current * total))

        # # To run another Processing algorithm as part of this algorithm, you can use
        # # processing.run(...). Make sure you pass the current context and feedback
        # # to processing.run to ensure that all temporary layer outputs are available
        # # to the executed algorithm, and that the executed algorithm can send feedback
        # # reports to the user (and correctly handle cancellation and progress reports!)
        # if False:
        #     buffered_layer = processing.run("native:buffer", {
        #         'INPUT': dest_id,
        #         'DISTANCE': 1.5,
        #         'SEGMENTS': 5,
        #         'END_CAP_STYLE': 0,
        #         'JOIN_STYLE': 0,
        #         'MITER_LIMIT': 2,
        #         'DISSOLVE': False,
        #         'OUTPUT': 'memory:'
        #     }, context=context, feedback=feedback)['OUTPUT']

        # # Return the results of the algorithm. In this case our only result is
        # # the feature sink which contains the processed features, but some
        # # algorithms may return multiple feature sinks, calculated numeric
        # # statistics, etc. These should all be included in the returned
        # # dictionary, with keys matching the feature corresponding parameter
        # # or output names.
        return {self.OUTPUT: dest_id}


# Used to develop together with plugin SCRIPT RUNNER

def run_script(iface):
    print("Script")
    ProfileLayer = ''
    DGMSource = ''
    print('In run script')

