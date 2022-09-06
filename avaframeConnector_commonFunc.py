# -*- coding: utf-8 -*-

import pathlib
import shutil

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
    
    for source in sourceDict:
        copyShp(source, targetPath) 

def copyShp(source, targetPath):
    ''' copies shapefile parts to targetPath
    
        Parameters
        -----------
        sourceDict: 
            qgis source of shapefile 
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
    """ Get all files of a shapefile"""

    globBase = base.parent
    globbed = globBase.glob(base.stem + '.*')

    return globbed
