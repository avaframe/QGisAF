# -*- coding: utf-8 -*-
import pathlib
import shutil
import pandas as pd
from avaframe.in3Utils import fileHandlerUtils as fU


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


def copyMultipleShp(sourceDict, targetPath):
    ''' copies multiple shapefile parts to targetPath
    
        Parameters
        -----------
        sourceDict: 
            dict with multiple qgis source of shapefiles (path string)
        targetPath: string
            path to where the files are being copied (directory) 
    '''
    for source in sourceDict:
        copyShp(source, targetPath) 


def copyShp(source, targetPath):
    ''' copies shapefile parts to targetPath
    
        Parameters
        -----------
        source: 
            qgis source of shapefile (path string)
        targetPath: string
            path to where the files are being copied (directory) 
    '''
    sourcePath = pathlib.Path(source)

    shpParts = getSHPParts(sourcePath)
    for shpPart in shpParts:
        try:
            shutil.copy(shpPart, targetPath)
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


