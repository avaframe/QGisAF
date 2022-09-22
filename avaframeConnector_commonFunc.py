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
