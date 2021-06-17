# -*- coding: utf-8 -*-
import pathlib
import shutil
import pandas
pandas.set_option('display.max_colwidth', 10)

 # qgis_process run script:avaframeqgis -- DEM=/home/felix/Versioning/AvaFrame/avaframe/data/avaSlide/Inputs/slideTopo.asc REL=/home/felix/Versioning/AvaFrame/avaframe/data/avaSlide/Inputs/REL/slideRelease.shp PROFILE=/home/felix/Versioning/AvaFrame/avaframe/data/avaSlide/Inputs/LINES/slideProfiles_AB.shp


from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsFeatureRequest,
                       QgsVectorLayer,
                       QgsProject,
                       QgsRasterLayer,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingContext,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterString,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingLayerPostProcessorInterface,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingOutputRasterLayer,
                       QgsProcessingOutputMultipleLayers,
                       QgsProcessingParameterFeatureSink)
from qgis import processing
import avaframe
from avaframe.in3Utils import initializeProject as iP
from avaframe import runOperational as runOp


class Renamer (QgsProcessingLayerPostProcessorInterface):
    def __init__(self, layer_name):
        self.name = layer_name
        super().__init__()

    def postProcessLayer(self, layer, context, feedback):
        layer.setName(self.name)

class AvaFrameQGis(QgsProcessingAlgorithm):

    DEM = 'DEM'
    REL = 'REL'
    PROFILE = 'PROFILE'
    SPLITPOINTS = 'SPLITPOINTS'
    OUTPUT = 'OUTPUT'
    OUTPPR = 'OUTPPR'
    FOLNAME = 'FOLNAME'
    SMALLAVA = 'SMALLAVA'

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

        self.addParameter(QgsProcessingParameterRasterLayer(
            self.DEM,
            self.tr("DEM layer")))

        self.addParameter(QgsProcessingParameterFeatureSource(
                self.REL,
                self.tr('Release layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            ))

        self.addParameter(QgsProcessingParameterString(
                self.FOLNAME,
                self.tr('Folder Name'),
                optional=True
            ))

        self.addParameter(QgsProcessingParameterBoolean(
                self.SMALLAVA,
                self.tr('Small Avalanche '),
                optional=True
            ))

        self.addParameter(QgsProcessingParameterFeatureSource(
            self.PROFILE,
            self.tr("Profile layer"),
            [QgsProcessing.TypeVectorLine]))

        self.addParameter(QgsProcessingParameterFeatureSource(
            self.SPLITPOINTS,
            self.tr("Splitpoint layer"),
            # defaultValue = 5,
            optional=True,
            types=[QgsProcessing.TypeVectorPoint]))

        # self.addParameter(QgsProcessingParameterFeatureSink(
        #     self.OUTPUT,
        #     self.tr("OUTPUT"),
        #     [QgsProcessing.TypeVectorAnyGeometry]))

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        # self.addParameter(
        #     # QgsProcessingParameterFeatureSink(
        #     QgsProcessingOutputVectorLayer(
        #         self.OUTPUT,
        #         self.tr('Output layer')
        #     )
        # )
        self.addOutput(QgsProcessingOutputVectorLayer(
            self.OUTPUT,
            self.tr("Output layer"),
            QgsProcessing.TypeVectorAnyGeometry))

        # self.addOutput(QgsProcessingOutputRasterLayer(
        #     self.OUTPPR,
        #     self.tr("PPR layer"),
        #     QgsProcessing.TypeRaster))

        self.addOutput(
        QgsProcessingOutputMultipleLayers(
                self.OUTPPR,
            )
        )

    def getSHPParts(self, base):
        """ Get all files of a shapefile"""

        globBase = base.parent
        globbed = globBase.glob(base.stem + '.*')

        return globbed

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        sourceDEM = self.parameterAsRasterLayer(parameters, self.DEM, context)
        if sourceDEM is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.DEM))

        sourceREL = self.parameterAsVectorLayer(parameters, self.REL, context)
        if sourceREL is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.REL))

        sourcePROFILE = self.parameterAsVectorLayer(parameters, self.PROFILE, context)
        if sourcePROFILE is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.PROFILE))

        sourceSPLITPOINTS= self.parameterAsVectorLayer(parameters, self.SPLITPOINTS, context)
        if sourceSPLITPOINTS is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.SPLITPOINTS))

        # create folder structure
        # TODO: make sure directory is empty
        targetDir = '/home/felix/tmp/TestAva2'
        iP.initializeFolderStruct(targetDir)

        feedback.pushInfo(sourceDEM.source())

        # copy DEM
        sourceDEMPath = pathlib.Path(sourceDEM.source())
        targetDEMPath = pathlib.Path(targetDir) / 'Inputs'
        try:
            shutil.copy(sourceDEMPath, targetDEMPath)
        except shutil.SameFileError:
            pass


        # copy all release shapefile parts
        sourceRELPath = pathlib.Path(sourceREL.source())
        targetRELPath = pathlib.Path(targetDir) / 'Inputs' / 'REL'

        shpParts = self.getSHPParts(sourceRELPath)
        for shpPart in shpParts:
            try:
                shutil.copy(shpPart, targetRELPath)
            except shutil.SameFileError:
                pass

        # copy all Profile shapefile parts
        sourcePROFILEPath = pathlib.Path(sourcePROFILE.source())
        targetPROFILEPath = pathlib.Path(targetDir) / 'Inputs' / 'LINES'

        shpParts = self.getSHPParts(sourcePROFILEPath)
        for shpPart in shpParts:
            try:
                shutil.copy(shpPart, targetPROFILEPath)
            except shutil.SameFileError:
                pass

        # copy all Splitpoint shapefile parts
        sourceSPLITPOINTSPath = pathlib.Path(sourceSPLITPOINTS.source())
        targetSPLITPOINTSPath = pathlib.Path(targetDir) / 'Inputs' / 'POINTS'

        shpParts = self.getSHPParts(sourceSPLITPOINTSPath)
        for shpPart in shpParts:
            try:
                shutil.copy(shpPart, targetSPLITPOINTSPath)
            except shutil.SameFileError:
                pass

        abResultsSource, rasterResults = runOp.runOperational(str(targetDir))

        shpLayer = str(abResultsSource) + '.shp'

        # The format is:
        # vlayer = QgsVectorLayer(data_source, layer_name, provider_name)

        source = QgsVectorLayer(shpLayer, "AlphaBeta", "ogr")


        # Copy input data
        feedback.pushInfo('Hallo')


        qmls = dict()
        qmls['ppr'] = './QGisStyles/ppr.qml'
        qmls['pfd'] = '/home/felix/Versioning/QGIS/Legends/ramms_MAXH.qml'
        qmls['pfv'] = './QGisStyles/pfv.qml'


        allRasterLayers = list()
        for index, row in rasterResults.iterrows():
            print(row["files"], row["resType"])
            rstLayer = QgsRasterLayer(str(row['files']), row['names'])
            rstLayer.loadNamedStyle(qmls[row['resType']])

            allRasterLayers.append(rstLayer)

        # should work, but doesn't...
        # rstLayer.setName('ThisIsDaStuff')


        # # Add SamosAT Group
        # Root = QgsProject.instance().layerTreeRoot()

        # # See if SamosAT group exists
        # # if not, create
        # SatGroup = Root.findGroup("com1DFA")
        # if SatGroup:
        #     feedback.pushDebugInfo('Found')
        # else:
        #     feedback.pushDebugInfo('Not Found')
        #     SatGroup = Root.insertGroup(0, "com1DFA")

        context.temporaryLayerStore().addMapLayers(allRasterLayers)

        for item in allRasterLayers:
            context.addLayerToLoadOnCompletion(
                item.id(),
                QgsProcessingContext.LayerDetails('raster layer',
                                              context.project(),
                                              self.OUTPPR))

        # context.addLayerToLoadOnCompletion(
        #     allRasterLayers[0].id(),
        #     QgsProcessingContext.LayerDetails('raster layer',
        #                                       context.project(),
        #                                       self.OUTPPR))

        # global renamer
        # renamer = Renamer('DiffBuf')

        context.temporaryLayerStore().addMapLayer(source)
        context.addLayerToLoadOnCompletion(
            source.id(),
            QgsProcessingContext.LayerDetails('OGR layer',
                                              context.project(),
                                              self.OUTPUT))

        # context.temporaryLayerStore().addMapLayer(rstLayer)
        # context.addLayerToLoadOnCompletion(
        #     rstLayer.id(),
        #     QgsProcessingContext.LayerDetails('raster layer',
        #                                       context.project(),
        #                                       self.OUTPPR))

        # context.layerToLoadOnCompletionDetails(rstLayer.id()).setPostProcessor(renamer)

        # self.ImportDFA(sourceDIR, Sim, SatGroup)

        # iface.layerTreeView().collapseAllNodes()

        return {self.OUTPUT: source, self.OUTPPR: allRasterLayers}
        # return {self.OUTPUT: source, self.OUTPPR: allRasterLayers[0]}

        # return {self.OUTPUT: source}


# Used to develop together with plugin SCRIPT RUNNER

def run_script(iface):
    print("Script")
    ProfileLayer = ''
    DGMSource = ''
    print('In run script')

