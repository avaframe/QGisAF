# -*- coding: utf-8 -*-
import pathlib
import shutil
import pandas as pd
import sys
from avaframe.in3Utils import fileHandlerUtils as fU
from avaframe.in3Utils import initializeProject as iP



def copyDEM(dem, targetDir):
    ''' copies the DEM to targetDir/Inputs
    
        Parameters
        -----------
        dem: 
            qgis source of dem
        targetDir: string
            base avalanche target directory 
    '''
    sourceDEMPath = pathlib.Path(dem.source())
    targetDEMPath = targetDir / 'Inputs'
    try:
        shutil.copy(sourceDEMPath, targetDEMPath)
    except shutil.SameFileError:
        pass


def copyMultipleShp(sourceDict, targetPath, addToName=''):
    ''' copies multiple shapefile parts to targetPath

        Parameters
        -----------
        sourceDict: 
            dict with multiple qgis source of shapefiles (path string)
        targetPath: string
            path to where the files are being copied (directory)
        addToName: string
            add this string to shape name
    '''
    for source in sourceDict:
        copyShp(source, targetPath, addToName)


def copyShp(source, targetPath, addToName=''):
    ''' copies shapefile parts to targetPath

        Parameters
        -----------
        source:
            qgis source of shapefile (path string)
        targetPath: string
            path to where the files are being copied (directory) 
        addToName: string
            add this string to shape name
    '''
    sourcePath = pathlib.Path(source)

    shpParts = getSHPParts(sourcePath)
    for shpPart in shpParts:
        nName = shpPart.stem + addToName + shpPart.suffix
        nTargetPath = targetPath / nName
        try:
            shutil.copy(shpPart, nTargetPath)
        except shutil.SameFileError:
            pass


def getSHPParts(base):
    '''Get all files of a shapefile

        Parameters
        -----------
        base: pathlib path 
            to .shp file
        Returns
        -------
        generator with all shapefile parts
    '''

    globBase = base.parent
    globbed = globBase.glob(base.stem + '.*')

    return globbed


def getLatestPeak(targetDir):
    '''Get latest peakFiles of com1DFA results

        Parameters
        -----------
        targetDir: pathlib path
            to avalanche directory
        Returns
        -------
        rasterResults: dataframe
            dataframe with info about simulations, including path
    '''
    avaDir = pathlib.Path(str(targetDir))
    inputDirPeak = avaDir / 'Outputs' / 'com1DFA' / 'peakFiles'
    allRasterResults = fU.makeSimDF(inputDirPeak, avaDir=avaDir)

    # Get info about latest simulations
    inputDirConf = avaDir / 'Outputs' / 'com1DFA' / 'configurationFiles'
    latestCsv = inputDirConf / 'latestSims.csv'
    with open(latestCsv, 'rb') as file:
        latestResults = pd.read_csv(file, index_col=0, keep_default_na=False)

    # Only use results from latest run
    rasterResults = allRasterResults[allRasterResults.simID.isin(latestResults.index)]

    return rasterResults


def getAlphaBetaResults(targetDir):
    '''Get results of com2AB

        Parameters
        -----------
        targetDir: pathlib path
            to avalanche directory
        Returns
        -------

    '''
    from qgis.core import (QgsVectorLayer)
    avaDir = pathlib.Path(str(targetDir))
    abResultsFile = avaDir / 'Outputs' / 'com2AB' / 'com2AB_Results.shp'

    if pathlib.Path.is_file(abResultsFile):
        abResultsLayer = QgsVectorLayer(str(abResultsFile), "AlphaBeta (com2)", "ogr")
        return abResultsLayer
    else:
        return 'None'


def getAna4ProbAnaResults(targetDir):
    '''Get results of ana4PropAna

        Parameters
        -----------
        targetDir: pathlib path
            to avalanche directory
        Returns
        -------

    '''
    from qgis.core import (QgsRasterLayer)
    avaDir = pathlib.Path(str(targetDir))
    ana4ResultsDir = avaDir / 'Outputs' / 'ana4Stats'

    globbed = ana4ResultsDir.glob(avaDir.stem + '*.asc')
    scriptDir = pathlib.Path(__file__).parent
    qml = str(scriptDir / 'QGisStyles' / 'probMap.qml')

    allRasterLayers = list()
    for item in globbed:
        rstLayer = QgsRasterLayer(str(item), item.stem)
        try:
            rstLayer.loadNamedStyle(qml)
        except:
            pass

        allRasterLayers.append(rstLayer)

    return allRasterLayers


def addStyleToCom1DFAResults(rasterResults):
    ''' add QML Style to com1DFA raster results

        Parameters
        -----------
        rasterResults: dict
            list of com1DFA results
        Returns
        -------
        allRasterLayers: list
            list of QGis raster layers with name and style

    '''
    from qgis.core import (QgsRasterLayer)

    scriptDir = pathlib.Path(__file__).parent
    qmls = dict()
    qmls['ppr'] = str(scriptDir / 'QGisStyles' / 'ppr.qml')
    qmls['pft'] = str(scriptDir / 'QGisStyles' / 'pft.qml')
    qmls['pfv'] = str(scriptDir / 'QGisStyles' / 'pfv.qml')
    qmls['PR'] = str(scriptDir / 'QGisStyles' / 'ppr.qml')
    qmls['FV'] = str(scriptDir / 'QGisStyles' / 'pfv.qml')
    qmls['FT'] = str(scriptDir / 'QGisStyles' / 'pft.qml')

    allRasterLayers = list()
    for index, row in rasterResults.iterrows():
        rstLayer = QgsRasterLayer(str(row['files']), row['names'])
        try:
            rstLayer.loadNamedStyle(qmls[row['resType']])
        except:
            pass

        allRasterLayers.append(rstLayer)

    return allRasterLayers


def addLayersToContext(context, layers, outTarget):
    ''' add multiple layers to qgis context

        Parameters
        -----------
        context: QGisProcessing context
        layers: list
            list of QGis layers to add
        Returns
        -------
        context:
            updated context
    '''
    from qgis.core import (QgsProcessingContext)

    context.temporaryLayerStore().addMapLayers(layers)

    for item in layers:
        context.addLayerToLoadOnCompletion(
            item.id(),
            QgsProcessingContext.LayerDetails(item.name(),
                                              context.project(),
                                              outTarget))

    return context


def addSingleLayerToContext(context, layer, outTarget):
    ''' add layer to qgis context

        Parameters
        -----------
        context: QGisProcessing context
        layer: Qgis layer
            QGis layer to add
        Returns
        -------
        context:
            updated context
    '''
    from qgis.core import (QgsProcessingContext)

    context.temporaryLayerStore().addMapLayer(layer)

    context.addLayerToLoadOnCompletion(
        layer.id(),
        QgsProcessingContext.LayerDetails(layer.name(),
                                          context.project(),
                                          outTarget))

    return context


def moveInputAndOutputFoldersToFinal(targetDir, finalTargetDir):
    ''' Move input and output folders to finalTargetDir

        Parameters
        -----------
        finalTargetDir: path
            The directory in which the final results will end up
        targetDir: path
            The same, but with /tmp added 
        Returns
        -------
    '''
    shutil.copytree(targetDir / 'Outputs', finalTargetDir / 'Outputs', dirs_exist_ok=True)
    shutil.rmtree(targetDir / 'Outputs')
    shutil.copytree(targetDir / 'Inputs', finalTargetDir / 'Inputs', dirs_exist_ok=True)
    shutil.rmtree(targetDir / 'Inputs')
    logFile = list(targetDir.glob('*.log'))
    shutil.move(logFile[0], finalTargetDir)

    # remove tmp directory
    shutil.rmtree(targetDir)

    return 'Success'

def createFolderStructure(foldDest):
    ''' create (tmp) folder structure

        Parameters
        -----------
        foldDest: path/str
            Destination folder
        Returns
        -------
        finalTargetDir: path
            The directory in which the final results will end up
        targetDir: path
            The same, but with /tmp added
    '''

    finalTargetDir = pathlib.Path(foldDest)
    targetDir = finalTargetDir / 'tmp'

    iP.initializeFolderStruct(targetDir, removeExisting=True)

    finalOutputs = finalTargetDir / 'Outputs'
    if finalOutputs.is_dir():
        shutil.copytree(finalOutputs, targetDir / 'Outputs', dirs_exist_ok=True)

    return(finalTargetDir, targetDir)
