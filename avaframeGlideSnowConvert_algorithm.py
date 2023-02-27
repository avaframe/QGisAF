# -*- coding: utf-8 -*-

"""
/***************************************************************************
 AvaFrameRunCom1DFA
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

__author__ = "AvaFrame Team"
__date__ = "2023"
__copyright__ = "(C) 2023 by AvaFrame Team"

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = "$Format:%H$"


import pandas
import os
import pathlib
from pathlib import Path

pandas.set_option("display.max_colwidth", 10)

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingContext,
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsProcessingException,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterFolderDestination,
    QgsProcessingOutputVectorLayer,
    QgsProcessingOutputMultipleLayers,
)

from qgis import processing


class AvaFrameGlideSnowConvertAlgorithm(QgsProcessingAlgorithm):
    """
    This is the AvaFrame Connection, i.e. the part running with QGis. For this
    connector to work, more installation is needed. See instructions at docs.avaframe.org
    """

    GSLAYERS = "GSLAYERS"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.GSLAYERS,
                self.tr("Glide snow layer(s)"),
                layerType=QgsProcessing.TypeRaster,
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

        # glide snow files
        allGS = self.parameterAsLayerList(parameters, self.GSLAYERS, context)
        if allGS is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.GSLAYERS))

        vectorResults = list()

        # Iterate through all raster layers
        for layer in allGS:

            # Get layer crs
            thisLayerCRS = layer.crs()

            # Get source layer dir
            cuLayerName = layer.name()
            sourcePath = Path(layer.source())
            sourceDir = sourcePath.parent
            sourceFileName = sourcePath.stem

            print('Layer name:', layer.name())

            # Set new layer name
            newLayerName = cuLayerName
            newLayerPath = sourceDir.joinpath(sourceFileName+'.shp')

            # fullOutput =  'ogr:dbname=\''+str(newLayerPath)+'\''
            # fullOutput =  str(newLayerPath)+'?a_srs="EPSG:27700"'
            # fullOutput =  'ogr:dbname=\''+str(newLayerPath)+'\' table=\"' + layer.name() + '\" (geom)'

            params = {'BAND': 1, 'CREATE_3D': False,
                      'EXTRA': '', 'FIELD_NAME': 'ELEV', 'IGNORE_NODATA': True,
                      'INPUT': layer,
                      'INTERVAL': 1, 'NODATA': None, 'OFFSET': 0.01,
                      # 'OUTPUT': fullOutput}
                      'OUTPUT': str(newLayerPath)}

            result = processing.run("gdal:contour", params)

            # print(result['OUTPUT'])
            vectorResults.append({'file': result['OUTPUT'],
                                  'name': newLayerName,
                                  'crs': thisLayerCRS})

        feedback.pushInfo("Done, start loading the results")

        # scriptDir = Path(__file__).parent
        # qmls = dict()
        # qmls["ppr"] = str(scriptDir / "QGisStyles" / "ppr.qml")
        # qmls["pft"] = str(scriptDir / "QGisStyles" / "pft.qml")
        # qmls["pfv"] = str(scriptDir / "QGisStyles" / "pfv.qml")
        # qmls["PR"] = str(scriptDir / "QGisStyles" / "ppr.qml")
        # qmls["FV"] = str(scriptDir / "QGisStyles" / "pfv.qml")
        # qmls["FT"] = str(scriptDir / "QGisStyles" / "pft.qml")

        allVectorLayers = list()
        for row in vectorResults:
            print(row["file"], row["name"])
            vectorLayer = QgsVectorLayer(row["file"], row["name"], "ogr")
            vectorLayer.setCrs(row["crs"])
            vectorLayer.setName(row["name"])
        #     rstLayer = QgsRasterLayer(str(row["files"]), row["names"])
        #     try:
        #         rstLayer.loadNamedStyle(qmls[row["resType"]])
        #     except:
        #         feedback.pushInfo("No matching layer style found")
        #         pass

            allVectorLayers.append(vectorLayer)

        context.temporaryLayerStore().addMapLayers(allVectorLayers)

        for item in allVectorLayers:
            context.addLayerToLoadOnCompletion(
                item.id(),
                QgsProcessingContext.LayerDetails(
                    item.name(), context.project(), self.OUTPUT
                ),
            )

        # feedback.pushInfo("\n---------------------------------")
        # feedback.pushInfo("Done, find results and logs here:")
        # feedback.pushInfo(str(targetDir.resolve()))
        # feedback.pushInfo("---------------------------------\n")

        return {self.OUTPUT: allVectorLayers}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "glidesnowconvert"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Glide snow convert")

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
        hstring = "Converts glide snow results from raster to contours. \n\
                For more information go to (or use the help button below): \n\
                AvaFrame Documentation: https://docs.avaframe.org\n\
                Homepage: https://avaframe.org\n\
                Praxisleitfaden: https://avaframe.org/reports\n"

        return self.tr(hstring)

    def helpUrl(self):
        return "https://docs.avaframe.org/en/latest/connector.html"

    def createInstance(self):
        return AvaFrameGlideSnowConvertAlgorithm()