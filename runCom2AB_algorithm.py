# -*- coding: utf-8 -*-

"""
/***************************************************************************
 AvaFrameRuncom2AB
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


import pathlib
import subprocess
import shutil
from pathlib import Path

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsRasterLayer,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingContext,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingOutputMultipleLayers)


class runCom2ABAlgorithm(QgsProcessingAlgorithm):
    """
    This is the AvaFrame Connection, i.e. the part running with QGis. For this
    connector to work, more installation is needed. See instructions at docs.avaframe.org
    """

    DEM = 'DEM'
    PROFILE = 'PROFILE'
    SPLITPOINTS = 'SPLITPOINTS'
    OUTPUT = 'OUTPUT'
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

        self.addParameter(QgsProcessingParameterFeatureSource(
            self.PROFILE,
            self.tr("Profile layer"),
            defaultValue="",
            types=[QgsProcessing.TypeVectorLine]))

        self.addParameter(QgsProcessingParameterFeatureSource(
            self.SPLITPOINTS,
            self.tr("Splitpoint layer"),
            defaultValue="",
            types=[QgsProcessing.TypeVectorPoint]))

#          self.addParameter(QgsProcessingParameterBoolean(
#                  self.SMALLAVA,
#                  self.tr('Small Avalanche (for com2AB) '),
#                  optional=True
#              ))

        self.addParameter(QgsProcessingParameterFolderDestination(
                self.FOLDEST,
                self.tr('Destination folder')
            ))

        self.addOutput(QgsProcessingOutputVectorLayer(
            self.OUTPUT,
            self.tr("Output layer"),
            QgsProcessing.TypeVectorAnyGeometry))

    def flags(self):
        return super().flags()
        # return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        from avaframe.in3Utils import initializeProject as iP
        import avaframe.version as gv
        from . import avaframeConnector_commonFunc as cF

        feedback.pushInfo('AvaFrame Version: ' + gv.getVersion())

        sourceDEM = self.parameterAsRasterLayer(parameters, self.DEM, context)
        if sourceDEM is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.DEM))

        sourceFOLDEST = self.parameterAsFile(parameters, self.FOLDEST, context)

        sourcePROFILE = self.parameterAsVectorLayer(parameters, self.PROFILE, context)

        sourceSPLITPOINTS = self.parameterAsVectorLayer(parameters, self.SPLITPOINTS, context)

        # create folder structure
        finalTargetDir = pathlib.Path(sourceFOLDEST)
        targetDir = finalTargetDir / 'tmp'
        iP.initializeFolderStruct(targetDir, removeExisting=True)

        finalOutputs = finalTargetDir / 'Outputs'
        if finalOutputs.is_dir():
            shutil.copytree(finalOutputs, targetDir / 'Outputs', dirs_exist_ok=True)

        feedback.pushInfo(sourceDEM.source())

        # copy DEM
        cF.copyDEM(sourceDEM, targetDir)

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

        feedback.pushInfo('Starting alpha beta')
        feedback.pushInfo('See console for progress')

        subprocess.call(['python', '-m', 'avaframe.runCom2AB', str(targetDir)])

        feedback.pushInfo('Done, start loading the results')

        # Move input and output folders to finalTargetDir
        shutil.copytree(targetDir / 'Outputs', finalTargetDir / 'Outputs', dirs_exist_ok=True)
        shutil.rmtree(targetDir / 'Outputs')
        shutil.copytree(targetDir / 'Inputs', finalTargetDir / 'Inputs', dirs_exist_ok=True)
        shutil.rmtree(targetDir / 'Inputs')
        logFile = list(targetDir.glob('*.log'))
        shutil.move(logFile[0], finalTargetDir)

        # Get alphabeta shapefile to return to QGIS
        abResultsLayer = cF.getAlphaBetaResults(finalTargetDir)

        context = cF.addSingleLayerToContext(context, abResultsLayer, self.OUTPUT)

        feedback.pushInfo('\n---------------------------------')
        feedback.pushInfo('Done, find results and logs here:')
        feedback.pushInfo(str(targetDir.resolve()))
        feedback.pushInfo('---------------------------------\n')

        return {self.OUTPUT: abResultsLayer}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'com2ab'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Alpha Beta (com2)')

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
        hstring = 'Runs alpha beta via module com2AB. \n\
                For more information go to (or use the help button below): \n\
                AvaFrame Documentation: https://docs.avaframe.org\n\
                Homepage: https://avaframe.org\n\
                Praxisleitfaden: https://avaframe.org/reports\n'

        return self.tr(hstring) 
                # Praxisleitfaden: https://info.bml.gv.at/dam/jcr:edebd872-2a86-4edf-ac5e-635ef11e35fe/Praxisleitfaden%20LawSim%20WLV%202022%20Gr%C3%BCn.pdf\n'

    def helpUrl(self):
        return "https://docs.avaframe.org/en/latest/connector.html"

    def createInstance(self):
        return runCom2ABAlgorithm()
