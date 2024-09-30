# -*- coding: utf-8 -*-

__author__ = "AvaFrame Team"
__date__ = "2022"
__copyright__ = "(C) 2022 by AvaFrame Team"

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = "$Format:%H$"

import subprocess
from pathlib import Path

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterEnum,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterFolderDestination,
    QgsProcessingOutputVectorLayer,
    QgsProcessingOutputMultipleLayers,
)


class runCom6RockAvalancheAlgorithm(QgsProcessingAlgorithm):
    """
    This is the AvaFrame Connection, i.e. the part running with QGis. For this
    connector to work, more installation is needed. See instructions at docs.avaframe.org
    """

    DEM = "DEM"
    REL = "REL"
    RELTH = "RELTH"
    SECREL = "SECREL"
    ENT = "ENT"
    RES = "RES"
    OUTPUT = "OUTPUT"
    OUTPPR = "OUTPPR"
    FOLDEST = "FOLDEST"
    DATA_TYPE = "DATA_TYPE"

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
            QgsProcessingParameterRasterLayer(
                self.RELTH, self.tr("Release thickness layer")
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.SECREL,
                self.tr("Secondary release layer (only one is allowed)"),
                optional=True,
                defaultValue="",
                types=[QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ENT,
                self.tr("Entrainment layer (only one is allowed)"),
                optional=True,
                defaultValue="",
                types=[QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.RES,
                self.tr("Resistance layer (only one is allowed)"),
                optional=True,
                defaultValue="",
                types=[QgsProcessing.TypeVectorAnyGeometry],
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

        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPPR,
            )
        )

    def flags(self):
        return super().flags()
        # return super().flags() | QgsProcessingAlgorithm.FlagNoThreading

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        import avaframe.version as gv
        from . import avaframeConnector_commonFunc as cF

        feedback.pushInfo("AvaFrame Version: " + gv.getVersion())

        targetADDTONAME = ""

        sourceDEM = self.parameterAsRasterLayer(parameters, self.DEM, context)
        if sourceDEM is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.DEM))

        sourceRELTH = self.parameterAsRasterLayer(parameters, self.RELTH, context)

        # Release files
        allREL = self.parameterAsLayerList(parameters, self.REL, context)
        if allREL is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.REL))

        relDict = {}
        if allREL:
            relDict = {lyr.source(): lyr for lyr in allREL}

        # Secondary release files
        sourceSecREL = self.parameterAsVectorLayer(parameters, self.SECREL, context)
        if sourceSecREL is not None:
            srInfo = "_sec" + Path(sourceSecREL.source()).stem
            targetADDTONAME = targetADDTONAME + srInfo

        sourceENT = self.parameterAsVectorLayer(parameters, self.ENT, context)

        sourceRES = self.parameterAsVectorLayer(parameters, self.RES, context)

        sourceFOLDEST = self.parameterAsFile(parameters, self.FOLDEST, context)

        # create folder structure (targetDir is the tmp one)
        finalTargetDir, targetDir = cF.createFolderStructure(sourceFOLDEST)

        feedback.pushInfo(sourceDEM.source())

        # copy DEM
        cF.copyDEM(sourceDEM, targetDir)

        # copy all release shapefile parts
        cF.copyMultipleShp(relDict, targetDir / "Inputs" / "REL", targetADDTONAME)

        # copy all secondary release shapefile parts
        if sourceSecREL is not None:
            cF.copyShp(sourceSecREL.source(), targetDir / "Inputs" / "SECREL")

        if sourceRELTH is not None:
            cF.copyShp(sourceRELTH.source(), targetDir / "Inputs" / "RELTH")

        # copy all entrainment shapefile parts
        if sourceENT is not None:
            cF.copyShp(sourceENT.source(), targetDir / "Inputs" / "ENT")

        # copy all resistance shapefile parts
        if sourceRES is not None:
            cF.copyShp(sourceRES.source(), targetDir / "Inputs" / "RES")

        feedback.pushInfo("Starting the simulations")
        feedback.pushInfo("This might take a while")
        feedback.pushInfo("See console for progress")

        subprocess.call(
            [
                "python",
                "-m",
                "avaframe.runCom6RockAvalanche",
                str(targetDir),
            ]
        )

        feedback.pushInfo("Done, start loading the results")

        # Move input, log and output folders to finalTargetDir
        cF.moveInputAndOutputFoldersToFinal(targetDir, finalTargetDir)

        # Get peakfiles to return to QGIS
        try:
            rasterResults = cF.getLatestPeak(finalTargetDir)
        except:
            raise QgsProcessingException(
                self.tr("Something went wrong with com6RockAvalanche, please check log files")
            )

        allRasterLayers = cF.addStyleToCom1DFAResults(rasterResults)

        context = cF.addLayersToContext(context, allRasterLayers, self.OUTPPR)

        feedback.pushInfo("\n---------------------------------")
        feedback.pushInfo("Done, find results and logs here:")
        feedback.pushInfo(str(finalTargetDir.resolve()))
        feedback.pushInfo("---------------------------------\n")

        return {self.OUTPPR: allRasterLayers}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "com6rockavalanche"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Rock Avalanche (com6)")

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
        hstring = "Runs rock avalanche simulations via module com6RockAvalanche, based on com1DFA. \n\
                For more information go to (or use the help button below): \n\
                AvaFrame Documentation: https://docs.avaframe.org\n\
                Homepage: https://avaframe.org\n\
                Praxisleitfaden: https://avaframe.org/reports\n"

        return self.tr(hstring)

    def helpUrl(self):
        return "https://docs.avaframe.org/en/latest/connector.html"

    def createInstance(self):
        return runCom6RockAvalancheAlgorithm()
