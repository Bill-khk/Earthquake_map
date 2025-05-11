@echo off 
set OSGEO4W_ROOT=C:\Program Files\QGIS
set path=%OSGEO4W_ROOT%\bin;%WINDIR%\system32;%WINDIR%;%WINDIR%\system32\WBem

call o4w_env.bat 
call qt5_env.bat
call py3_env.bat

@echo off
path %OSGEO4W_ROOT%\apps\qgis-ltr\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis-ltr
set GDAL_FILENAME_IS_UTF8=YES
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr\qtplugins;%QT_PLUGIN_PATH%
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-ltr\python;%PYTHONPATH%

set PYCHARM="C:\Program Files\JetBrains\PyCharm Community Edition 2024.1.2\bin\pycharm64.exe"
@echo on
start "PyCharm with QGIS knowledge!" /B %PYCHARM% %*