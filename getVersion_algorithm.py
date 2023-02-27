# -*- coding: utf-8 -*-

"""
/***************************************************************************
GetVersion
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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterString,
)


class getVersionAlgorithm(QgsProcessingAlgorithm):
    """
    Rename avaframe layers by adding choosen parameters and their values
    """

    INPUT = 'INPUT'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(QgsProcessingParameterString(
                self.INPUT,
                self.tr('Dummy input'),
                optional=True,
                defaultValue="No need to add anything"
            ))

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        import avaframe.version as gv

        feedback.pushInfo('---------------')
        feedback.pushInfo('AvaFrame Version: ' + gv.getVersion())
        feedback.pushInfo('---------------')
        feedback.pushInfo('')

        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'GetVersion'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

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
        return 'Admin'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def shortHelpString(self) -> str:
        hstring = 'Returns the version of AvaFrame. \n\
                The input is purely a dummy input, needed for this \
                window to show up. \n\
                No need to add anything.'

        return self.tr(hstring)

    def helpUrl(self):
        return "https://docs.avaframe.org/en/latest/connector.html"

    def createInstance(self):
        return getVersionAlgorithm()