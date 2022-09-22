''' Tests for module common functions'''
import pytest
import pathlib
import os

# Local imports
from .. import avaframeConnector_commonFunc as cF 


def test_getSHPParts(tmp_path):
    """ test getSHPParts"""

    cwd = os.getcwd()
    inputDir = pathlib.Path(cwd)
    print(inputDir)
    shpParts = cF.getSHPParts(inputDir / 'Inputs' / 'REL' / 'slideRelease.shp')
    extensions = list()
    for ele in shpParts:
        extensions.append(ele.suffix)

    assert len(extensions) == 5
    assert '.prj' in extensions
    assert '.cpg' in extensions
    assert '.shx' in extensions
    assert '.dbf' in extensions
    assert '.shp' in extensions
