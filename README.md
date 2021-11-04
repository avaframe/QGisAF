# QGisAF
The QGis to AvaFrame Connector, providing the necessary files to be loaded in
QGis. See https://docs.avaframe.org/en/latest/ for more information regarding
installation and usage.

### License 
Licensed with [![European Public License EUPL](https://img.shields.io/badge/license-EUPL-green.png)](https://git.avaframe.org/AvaFrame/AvaFrame/src/branch/master/LICENSE.txt)


### For development: 

it is possible to install qgis in a conda enviroment:
conda install qgis --channel conda-forge

### To deploy

- change version info in `metadata.txt`

- use `pb_tool zip` to generate uploadable zip

- Upload to https://plugins.qgis.org
