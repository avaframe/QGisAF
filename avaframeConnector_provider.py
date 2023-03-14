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

__author__ = "AvaFrame Team"
__date__ = "2022-08-26"
__copyright__ = "(C) 2022 by AvaFrame Team"

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = "$Format:%H$"

import sys
import os.path
import subprocess
import os
import inspect
from qgis.core import Qgis
from qgis.core import QgsProcessingProvider
from qgis.core import QgsProcessingFeedback
from qgis.PyQt.QtGui import QIcon
from pathlib import Path

from qgis.core import (
    QgsMessageLog,
    QgsGeometry,
)

from qgis.PyQt.QtWidgets import (
    QMessageBox,
)

# Check for avaframe, if not available, install...
# Note: not the best solution (okok, it is utterly disgustingly hacky), but the only one available atm (Sep 2022)
def find_python():
    if sys.platform != "win32":
        return sys.executable

    for path in sys.path:  # searching sys.path for python executables
        assumed_path = os.path.join(path, "python.exe")
        print(assumed_path)
        if os.path.isfile(assumed_path):
            return assumed_path

    raise Exception("Python executable not found")


try:
    import avaframe
except ModuleNotFoundError:
    subprocess.call(["pip3", "install", "--upgrade", "--user", "pandas", "numpy"])
    subprocess.call(["pip3", "install", "avaframe", "--user"])
    try:
        import avaframe
    except ModuleNotFoundError:
        QMessageBox.information(
            None, "INFO", "Please restart QGis to finalize AvaFrame installation"
        )

# catch annoying ValueError from cython
# try:
#     from .avaframeConnector_algorithm import AvaFrameConnectorAlgorithm
#     from .avaframeLayerRename_algorithm import AvaFrameLayerRenameAlgorithm
#     from .avaframeGetVersion_algorithm import AvaFrameGetVersionAlgorithm
#     from .avaframeRunCom1DFA_algorithm import AvaFrameRunCom1DFAAlgorithm
# except ValueError:
#     python_exe = find_python()
#     subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", "--user", "pandas", "numpy"])
# End of hacky solution...

from .avaframeConnector_algorithm import AvaFrameConnectorAlgorithm
from .layerRename_algorithm import layerRenameAlgorithm
from .getVersion_algorithm import getVersionAlgorithm
from .runCom1DFA_algorithm import runCom1DFAAlgorithm
from .runCom5GlideSnow_algorithm import runCom5GlideSnowAlgorithm
# from .runAna4ProbAna_algorithm import runAna4ProbAnaAlgorithm
from .update_algorithm import updateAlgorithm


class AvaFrameConnectorProvider(QgsProcessingProvider):
    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)

    def flags(self):
        # return super().flags() | QgsProcessingAlgorithm.FlagNoThreading
        return super().flags()

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        self.addAlgorithm(AvaFrameConnectorAlgorithm())
        self.addAlgorithm(layerRenameAlgorithm())
        self.addAlgorithm(runCom1DFAAlgorithm())
        self.addAlgorithm(runCom5GlideSnowAlgorithm())
        self.addAlgorithm(runAna4ProbAnaAlgorithm())
        self.addAlgorithm(AvaFrameGlideSnowConvertAlgorithm())
        self.addAlgorithm(getVersionAlgorithm())
        self.addAlgorithm(updateAlgorithm())

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return "AVAFRAME"

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr("AVAFRAME")

    def icon(self):
        """
        Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, "icon.png")))
        return icon

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
