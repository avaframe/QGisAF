# -*- coding: utf-8 -*-

"""
/***************************************************************************
 AvaFrameRunCom1DFA
                                 A QGIS plugin
                              -------------------
        begin                : 2023-05-02
        copyright            : (C) 2023 by AvaFrame Team
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

__author__ = "AvaFrame Team"
__date__ = "2023"
__copyright__ = "(C) 2023 by AvaFrame Team"

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = "$Format:%H$"


import pathlib
import subprocess


from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingAlgorithm,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterFolderDestination,
    QgsProcessingOutputVectorLayer,
)


class runIn1RelInfoAlgorithm(QgsProcessingAlgorithm):
    """
    This is the AvaFrame Connection, i.e. the part running with QGis. For this
    connector to work, more installation is needed. See instructions at docs.avaframe.org
    """

    DEM = "DEM"
    REL = "REL"
    OUTPUT = "OUTPUT"
    FOLDEST = "FOLDEST"

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterRasterLayer(self.DEM, self.tr("DEM layer"))
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.REL,
                self.tr("Release layer(s)"),
                layerType=QgsProcessing.TypeVectorAnyGeometry,
            )
        )

        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.FOLDEST, self.tr("Destination folder")
            )
        )

        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT,
                self.tr("Output layer"),
                QgsProcessing.TypeVectorAnyGeometry,
            )
        )

    def flags(self):
        return super().flags()
        # return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        from avaframe.in3Utils import initializeProject as iP
        from avaframe import runIn1RelInfo as runRelInfo
        import avaframe.version as gv
        from . import avaframeConnector_commonFunc as cF

        feedback.pushInfo("AvaFrame Version: " + gv.getVersion())

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

        sourceFOLDEST = self.parameterAsFile(parameters, self.FOLDEST, context)

        # create folder structure
        targetDir = pathlib.Path(sourceFOLDEST)
        iP.initializeFolderStruct(targetDir, removeExisting=False)

        feedback.pushInfo(sourceDEM.source())

        # copy DEM
        cF.copyDEM(sourceDEM, targetDir)

        # copy all release shapefile parts
        cF.copyMultipleShp(relDict, targetDir / "Inputs" / "REL")

        feedback.pushInfo("Starting the simulations")
        feedback.pushInfo("This might take a while")
        feedback.pushInfo("See console for progress")

        # Generate command and run via subprocess
        command = ['python', '-m', 'avaframe.runIn1RelInfo', str(targetDir)]
        cF.runAndCheck(command, self, feedback)

        resDir = targetDir / "Outputs" / "com1DFA" / "releaseInfoFile"

        feedback.pushInfo("\n---------------------------------")
        feedback.pushInfo("Done, find results and logs here:")
        feedback.pushInfo(str(targetDir.resolve()))
        feedback.pushInfo("Find the release area info file here:")
        feedback.pushInfo(str(resDir.resolve()))

        feedback.pushInfo("---------------------------------\n")

        return {}
        # return {self.OUTPUT: rasterResults}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "in1relinfo"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Release area stats(in1, com1)")

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
        return "Experimental"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def shortHelpString(self) -> str:
        hstring = "Returns info for release area statistics in a csv file. \n\
                For more information go to (or use the help button below): \n\
                AvaFrame Documentation: https://docs.avaframe.org\n\
                Homepage: https://avaframe.org\n\
                Praxisleitfaden: https://avaframe.org/reports\n"

        return self.tr(hstring)

    def helpUrl(self):
        return "https://docs.avaframe.org/en/latest/connector.html"

    def createInstance(self):
        return runIn1RelInfoAlgorithm()
