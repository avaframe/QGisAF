# -*- coding: utf-8 -*-
import shutil
import pandas
import pathlib
from pathlib import Path
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
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingParameterFolderDestination,
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
    ENT = 'ENT'
    RES = 'RES'
    PROFILE = 'PROFILE'
    SPLITPOINTS = 'SPLITPOINTS'
    OUTPUT = 'OUTPUT'
    OUTPPR = 'OUTPPR'
    FOLDEST = 'FOLDEST'
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

        # self.addParameter(QgsProcessingParameterFeatureSource(
        #         self.REL,
        #         self.tr('Release layer'),
        #         [QgsProcessing.TypeVectorAnyGeometry]
        #     ))
        self.addParameter(QgsProcessingParameterMultipleLayers(
                self.REL,
                self.tr('Release layer(s)'),
                layerType=QgsProcessing.TypeVectorAnyGeometry
            ))

        self.addParameter(QgsProcessingParameterFeatureSource(
            self.PROFILE,
            self.tr("Profile layer"),
            [QgsProcessing.TypeVectorLine]))

        self.addParameter(QgsProcessingParameterFeatureSource(
            self.SPLITPOINTS,
            self.tr("Splitpoint layer"),
            # defaultValue = 5,
            optional=False,
            types=[QgsProcessing.TypeVectorPoint]))


        self.addParameter(QgsProcessingParameterFolderDestination(
                self.FOLDEST,
                self.tr('Destination folder')
            ))

        self.addParameter(QgsProcessingParameterFeatureSource(
                self.ENT,
                self.tr('Entrainment layer'),
                optional=True,
                types=[QgsProcessing.TypeVectorAnyGeometry]
            ))

        self.addParameter(QgsProcessingParameterFeatureSource(
                self.RES,
                self.tr('Resistance layer'),
                optional=True,
                types=[QgsProcessing.TypeVectorAnyGeometry]
            ))

        self.addParameter(QgsProcessingParameterBoolean(
                self.SMALLAVA,
                self.tr('Small Avalanche (for com2AB) '),
                optional=True
            ))

        self.addOutput(QgsProcessingOutputVectorLayer(
            self.OUTPUT,
            self.tr("Output layer"),
            QgsProcessing.TypeVectorAnyGeometry))

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


        allREL = self.parameterAsLayerList(parameters, self.REL, context)
        if allREL is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.REL))

        relDict = {}
        if allREL:
            relDict = {lyr.source(): lyr for lyr in allREL}

        sourceENT = self.parameterAsVectorLayer(parameters, self.ENT, context)

        sourceFOLDEST = self.parameterAsFile(parameters, self.FOLDEST, context)

        sourcePROFILE = self.parameterAsVectorLayer(parameters, self.PROFILE, context)
        # if sourcePROFILE is None:
        #     raise QgsProcessingException(self.invalidSourceError(parameters, self.PROFILE))

        sourceSPLITPOINTS= self.parameterAsVectorLayer(parameters, self.SPLITPOINTS, context)
        # if sourceSPLITPOINTS is None:
        #     raise QgsProcessingException(self.invalidSourceError(parameters, self.SPLITPOINTS))

        # create folder structure
        # TODO: make sure directory is empty
        # targetDir = pathlib.Path('.') / 'TestDir'
        targetDir = pathlib.Path(sourceFOLDEST)
        iP.initializeFolderStruct(targetDir, removeExisting=True)

        feedback.pushInfo(sourceDEM.source())

        # copy DEM
        sourceDEMPath = pathlib.Path(sourceDEM.source())
        targetDEMPath = targetDir / 'Inputs'
        try:
            shutil.copy(sourceDEMPath, targetDEMPath)
        except shutil.SameFileError:
            pass

        # copy all release shapefile parts
        for sourceREL in relDict:
            sourceRELPath = pathlib.Path(sourceREL)
            targetRELPath = targetDir / 'Inputs' / 'REL'

            shpParts = self.getSHPParts(sourceRELPath)
            for shpPart in shpParts:
                try:
                    shutil.copy(shpPart, targetRELPath)
                except shutil.SameFileError:
                    pass

        # copy all entrainment shapefile parts
        if sourceENT is not None:
            sourceENTPath = pathlib.Path(sourceENT.source())
            targetENTPath = targetDir / 'Inputs' / 'ENT'

            shpParts = self.getSHPParts(sourceENTPath)
            for shpPart in shpParts:
                try:
                    shutil.copy(shpPart, targetENTPath)
                except shutil.SameFileError:
                    pass

        # copy all Profile shapefile parts
        sourcePROFILEPath = pathlib.Path(sourcePROFILE.source())
        targetPROFILEPath = targetDir / 'Inputs' / 'LINES'

        shpParts = self.getSHPParts(sourcePROFILEPath)
        for shpPart in shpParts:
            try:
                shutil.copy(shpPart, targetPROFILEPath)
            except shutil.SameFileError:
                pass

        # copy all Splitpoint shapefile parts
        sourceSPLITPOINTSPath = pathlib.Path(sourceSPLITPOINTS.source())
        targetSPLITPOINTSPath = targetDir / 'Inputs' / 'POINTS'

        shpParts = self.getSHPParts(sourceSPLITPOINTSPath)
        for shpPart in shpParts:
            try:
                shutil.copy(shpPart, targetSPLITPOINTSPath)
            except shutil.SameFileError:
                pass

        feedback.pushInfo('Starting the simulations')

        abResultsSource, rasterResults = runOp.runOperational(str(targetDir))

        shpLayer = str(abResultsSource) + '.shp'

        source = QgsVectorLayer(shpLayer, "AlphaBeta", "ogr")

        scriptDir = Path(__file__).parent
        qmls = dict()
        qmls['ppr'] = str(scriptDir / 'QGisStyles' / 'ppr.qml')
        qmls['pfd'] = str(scriptDir / 'QGisStyles' / 'pfd.qml')
        qmls['pfv'] = str(scriptDir / 'QGisStyles' / 'pfv.qml')

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

        feedback.pushInfo('\n---------------------------------')
        feedback.pushInfo('Done, find results and logs here:')
        feedback.pushInfo(str(targetDir.resolve()))
        feedback.pushInfo('---------------------------------\n')


        return {self.OUTPUT: source, self.OUTPPR: allRasterLayers}
        # return {self.OUTPUT: source, self.OUTPPR: allRasterLayers[0]}

        # return {self.OUTPUT: source}


# Used to develop together with plugin SCRIPT RUNNER

def run_script(iface):
    print("Script")
    ProfileLayer = ''
    DGMSource = ''
    print('In run script')
