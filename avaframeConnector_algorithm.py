# -*- coding: utf-8 -*-

"""
/***************************************************************************
 AvaFrameConnector
                                 A QGIS plugin
 Connects to AvaFrame
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-08-26
        copyright            : (C) 2021 by AvaFrame Team
        email                : felix@avaframe.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'AvaFrame Team'
__date__ = '2022'
__copyright__ = '(C) 2022 by AvaFrame Team'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import shutil
import pandas
import pathlib
from pathlib import Path
pandas.set_option('display.max_colwidth', 10)

#qgis_process run AVAFRAME:AvaFrameConnector -- DEM=/home/felix/tmp/WebinarAvaFrameExample/avaAlr/Inputs/avaAlr.asc ENT FOLDEST=/home/felix/tmp/Out1 PROFILE=/home/felix/tmp/WebinarAvaFrameExample/avaAlr/Inputs/LINES/pathAB.shp REL=/home/felix/tmp/WebinarAvaFrameExample/avaAlr/Inputs/REL/relAlr12.shp RES= SPLITPOINTS=/home/felix/tmp/WebinarAvaFrameExample/avaAlr/Inputs/POINTS/splitPoint.sh


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



class AvaFrameConnectorAlgorithm(QgsProcessingAlgorithm):
    """
    This is the AvaFrame Connection, i.e. the part running with QGis. For this
    connector to work, more installation is needed. See instructions at docs.avaframe.org
    """

    DEM = 'DEM'
    REL = 'REL'
    SECREL = 'SECREL'
    ENT = 'ENT'
    RES = 'RES'
    PROFILE = 'PROFILE'
    SPLITPOINTS = 'SPLITPOINTS'
    OUTPUT = 'OUTPUT'
    OUTPPR = 'OUTPPR'
    FOLDEST = 'FOLDEST'
    SMALLAVA = 'SMALLAVA'


    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(QgsProcessingParameterRasterLayer(
            self.DEM,
            self.tr("DEM layer")))

        #  self.addParameter(QgsProcessingParameterFeatureSource(
               #  self.REL,
               #  self.tr('Release layer'),
               #  [QgsProcessing.TypeVectorAnyGeometry]
           #  ))
        self.addParameter(QgsProcessingParameterMultipleLayers(
            self.REL,
            self.tr('Release layer(s)'),
            layerType=QgsProcessing.TypeVectorAnyGeometry
            ))
        
        self.addParameter(QgsProcessingParameterMultipleLayers(
            self.SECREL,
            self.tr('Secondary release layer(s)'),
            optional=True,
            defaultValue = "",
            layerType=QgsProcessing.TypeVectorAnyGeometry
            ))

        self.addParameter(QgsProcessingParameterFeatureSource(
                self.ENT,
                self.tr('Entrainment layer'),
                optional=True,
                defaultValue = "",
                types=[QgsProcessing.TypeVectorAnyGeometry]
            ))

        self.addParameter(QgsProcessingParameterFeatureSource(
                self.RES,
                self.tr('Resistance layer'),
                optional=True,
                defaultValue = "",
                types=[QgsProcessing.TypeVectorAnyGeometry]
            ))

        self.addParameter(QgsProcessingParameterFeatureSource(
            self.PROFILE,
            self.tr("Profile layer"),
            optional=True,
            defaultValue = "",
            types=[QgsProcessing.TypeVectorLine]))

        self.addParameter(QgsProcessingParameterFeatureSource(
            self.SPLITPOINTS,
            self.tr("Splitpoint layer"),
            defaultValue = "",
            optional=True,
            types=[QgsProcessing.TypeVectorPoint]))


        self.addParameter(QgsProcessingParameterFolderDestination(
                self.FOLDEST,
                self.tr('Destination folder')
            ))

   #          self.addParameter(QgsProcessingParameterBoolean(
#                  self.SMALLAVA,
#                  self.tr('Small Avalanche (for com2AB) '),
#                  optional=True
#              ))
#  #
        self.addOutput(QgsProcessingOutputVectorLayer(
            self.OUTPUT,
            self.tr("Output layer"),
            QgsProcessing.TypeVectorAnyGeometry))

        self.addOutput(
        QgsProcessingOutputMultipleLayers(
                self.OUTPPR,
            )
        )
#


    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        from avaframe.in3Utils import initializeProject as iP
        from avaframe import runOperational as runOp
        import avaframe.version as gv
        from . import avaframeConnector_commonFunc as cF 

        feedback.pushInfo('AvaFrame Version: ' + gv.getVersion())

        sourceDEM = self.parameterAsRasterLayer(parameters, self.DEM, context)
        if sourceDEM is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.DEM))

        # Release files
        allREL = self.parameterAsLayerList(parameters, self.REL, context)
        if allREL is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.REL))

        relDict = {}
        if allREL:
            relDict = {lyr.source(): lyr for lyr in allREL}

        # Secondary release files
        allSecREL = self.parameterAsLayerList(parameters, self.SECREL, context)

        secRelDict = {}
        if allSecREL:
            secRelDict = {lyr.source(): lyr for lyr in allSecREL}


        sourceENT = self.parameterAsVectorLayer(parameters, self.ENT, context)

        sourceRES = self.parameterAsVectorLayer(parameters, self.RES, context)

        sourceFOLDEST = self.parameterAsFile(parameters, self.FOLDEST, context)

        sourcePROFILE = self.parameterAsVectorLayer(parameters, self.PROFILE, context)

        sourceSPLITPOINTS= self.parameterAsVectorLayer(parameters, self.SPLITPOINTS, context)

        # create folder structure
        targetDir = pathlib.Path(sourceFOLDEST)
        iP.initializeFolderStruct(targetDir, removeExisting=False)

        feedback.pushInfo(sourceDEM.source())

        # copy DEM
        cF.copyDEM(sourceDEM, targetDir)

        # copy all release shapefile parts
        cF.copyMultipleShp(relDict, targetDir / 'Inputs' / 'REL')
       
        # copy all secondary release shapefile parts
        cF.copyMultipleShp(secRelDict, targetDir / 'Inputs' / 'SECREL')

        # copy all entrainment shapefile parts
        if sourceENT is not None:
            cF.copyShp(sourceENT.source(), targetDir / 'Inputs' / 'ENT')

        # copy all resistance shapefile parts
        if sourceRES is not None:
            cF.copyShp(sourceRES.source(), targetDir / 'Inputs' / 'RES')
        
        # copy all Splitpoint shapefile parts
        if sourceSPLITPOINTS is not None:
            cF.copyShp(sourceSPLITPOINTS.source(), targetDir / 'Inputs' / 'POINTS')

        # copy all Profile shapefile parts
        if sourcePROFILE is not None:
            sourcePROFILEPath = pathlib.Path(sourcePROFILE.source())
            targetPROFILEPath = targetDir / 'Inputs' / 'LINES'

            shpParts = cF.getSHPParts(sourcePROFILEPath)

            for shpPart in shpParts:
                try:
                    # make sure this file contains AB (for com2AB)
                    if 'AB' not in str(shpPart):
                        newName = shpPart.stem + '_AB' + shpPart.suffix
                        newName = targetPROFILEPath / newName
                        shutil.copy(shpPart, newName)
                    else:
                        shutil.copy(shpPart, targetPROFILEPath)
                except shutil.SameFileError:
                    pass

        feedback.pushInfo('Starting the simulations')
        feedback.pushInfo('This might take a while')
        feedback.pushInfo('Open Plugins -> Python Console to see the progress')

        abResultsSource, rasterResults = runOp.runOperational(str(targetDir))

        feedback.pushInfo('Done, start loading the results')
        
        if abResultsSource == 'None':
            source = None
            feedback.pushInfo('Alpha Beta was not run')
        else:
            feedback.pushInfo('Found ab source')
            shpLayer = str(abResultsSource) + '.shp'

            source = QgsVectorLayer(shpLayer, "AlphaBeta", "ogr")


        scriptDir = Path(__file__).parent
        qmls = dict()
        qmls['ppr'] = str(scriptDir / 'QGisStyles' / 'ppr.qml')
        # qmls['pft'] = str(scriptDir / 'QGisStyles' / 'pft.qml')
        qmls['pfv'] = str(scriptDir / 'QGisStyles' / 'pfv.qml')
        qmls['PR'] = str(scriptDir / 'QGisStyles' / 'ppr.qml')
        qmls['FV'] = str(scriptDir / 'QGisStyles' / 'pfv.qml')
        # qmls['FT'] = str(scriptDir / 'QGisStyles' / 'pft.qml')

        allRasterLayers = list()
        for index, row in rasterResults.iterrows():
            print(row["files"], row["resType"])
            rstLayer = QgsRasterLayer(str(row['files']), row['names'])
            try:
                rstLayer.loadNamedStyle(qmls[row['resType']])
            except:
                feedback.pushInfo('No matching layer style found')
                pass

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

        if source is not None:
            context.temporaryLayerStore().addMapLayer(source)
            context.addLayerToLoadOnCompletion(
                source.id(),
                QgsProcessingContext.LayerDetails('OGR layer',
                                                  context.project(),
                                                  self.OUTPUT))


        feedback.pushInfo('\n---------------------------------')
        feedback.pushInfo('Done, find results and logs here:')
        feedback.pushInfo(str(targetDir.resolve()))
        feedback.pushInfo('---------------------------------\n')


        if source is None:
            return {self.OUTPPR: allRasterLayers}
        else:
            return {self.OUTPUT: source, self.OUTPPR: allRasterLayers}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'fulloperationalrun'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Full Operational Run')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Operational'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def shortHelpString(self) -> str:
        hstring = 'Runs the operational workflow (com1DFA and com2AB). \n\
                For more information go to: \n\
                AvaFrame Documentation: https://docs.avaframe.org\n\
                Homepage: https://avaframe.org\n\
                Praxisleitfaden: https://avaframe.org/reports\n'

        return self.tr(hstring) 

    def helpUrl(self):
        return "https://docs.avaframe.org/en/latest/connector.html"

    def createInstance(self):
        return AvaFrameConnectorAlgorithm()
