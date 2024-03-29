# -*- coding: utf-8 -*-

"""
/***************************************************************************
 layerRename
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

import pandas
import pathlib
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProject,
    QgsProcessingException,
    QgsProcessingAlgorithm,
    QgsProcessingParameterString,
    QgsProcessingParameterMultipleLayers,
)
from qgis import processing


class layerRenameAlgorithm(QgsProcessingAlgorithm):
    """
    Rename avaframe layers by adding choosen parameters and their values
    """

    LAYERS = 'LAYERS'
    VARS = 'VARS'


    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(QgsProcessingParameterMultipleLayers(
                self.LAYERS,
                self.tr('Layer(s) to rename'),
                layerType=QgsProcessing.TypeMapLayer
            ))

        self.addParameter(QgsProcessingParameterString(
                self.VARS,
                self.tr('Comma separated list (no spaces) of parameters to add to name'),
                ''
            ))


    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        import avaframe.version as gv
        from avaframe.in3Utils import cfgHandling

        feedback.pushInfo('AvaFrame Version: ' + gv.getVersion())

        #for Testing, together with:
        # ➜ qgis_process run AVAFRAME:layerRename --project_path=/home/felix/tmp/TestProj.qgz -- LAYERS=  VARS='mu'
        project = QgsProject().instance()
        #  allLay = project.mapLayers().values()

        allLay = self.parameterAsLayerList(parameters, self.LAYERS, context)
        if allLay is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.LAYERS))
#
        vars = self.parameterAsString(parameters, self.VARS, context)

        feedback.pushInfo(vars)

        # Get a list of avaDirs to get the rename info from
        avaDirList = list()
        toRenameList = list()
        for layer in allLay:
            layerPath = layer.dataProvider().dataSourceUri()
            print(layer.dataProvider().dataSourceUri())
            lookFor = ['com1DFA','peakFiles','Outputs']
            if all(x in layerPath for x in lookFor):
                #checkIfAlreadyRenamed(layerPath)
                print('Seems to be a AvaFrame file')
                avaDir = layerPath.split('Outputs')[0]
                avaDirList.append(avaDir)
                toRenameList.append(layer)

        # make the list unique
        avaDirs = list(set(avaDirList))

        # get rename info
        allRenameDF = pandas.DataFrame()
        for avaDir in avaDirs:
            avaDir = pathlib.Path(avaDir)
            renameDF = cfgHandling.addInfoToSimName(avaDir,vars)
            allRenameDF = pandas.concat([allRenameDF, renameDF])

        # Loop through layers again, this time renaming
        for layer in toRenameList:
            layerPath = layer.dataProvider().dataSourceUri()
            name = layer.name()
            feedback.pushInfo(name)
            # get variable type by splitting at last underscore
            simName, delim, varType = name.rpartition('_')

            # find corresponding simName
            dfRow = allRenameDF.loc[allRenameDF['simName'] == simName]

            # take newName and readd variable type
            try:
                newLayerName = dfRow['newName'].values[0] + '_' + varType
                layer.setName(newLayerName)
            except IndexError:
                feedback.pushInfo('Layer already renamed?')

        return {}


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'layerRename'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Layer rename')

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
        return 'Experimental'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def shortHelpString(self) -> str:
        hstring = 'Renames com1DFA result layers by adding the values of the\
                given variable (from the configuration file). \n\
                For more information go to (or use the help button below): \n\
                AvaFrame Documentation: https://docs.avaframe.org\n\
                '

        return self.tr(hstring)

    def helpUrl(self):
        return "https://docs.avaframe.org/en/latest/connector.html"

    def createInstance(self):
        return layerRenameAlgorithm()
