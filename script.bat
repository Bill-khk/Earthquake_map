@echo off 
SET OSGEO4W_ROOT=C:\OSGeo4W

call "%OSGEO4W_ROOT%"\bin\o4w_env.bat
call "%OSGEO4W_ROOT%"\apps\grass\grass84\etc\env.bat

echo off
SET path %PATH%;%OSGEO4W_ROOT%\apps\qgis-ltr\bin
SET path %PATH%;%OSGEO4W_ROOT%\bin
SET path %PATH%;%OSGEO4W_ROOT%\apps\grass\grass84\lib
SET path %PATH%;C:\OSGeo4W\apps\Qt5\bin
SET path %PATH%;C:\OSGeo4W%\apps\Python312\Scripts
SET path %PATH%;C:\OSGeo4W%\apps\Python312

SET PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis-ltr\python;%OSGEO4W_ROOT%\apps\qgis-ltr\python\plugins
SET PYTHONHOME=%OSGEO4W_ROOT%\apps\Python312

set PYCHARM="C:\Program Files\JetBrains\PyCharm Community Edition 2024.1.2\bin\pycharm64.exe"
@echo on
start "PyCharm with QGIS knowledge!" /B %PYCHARM% %*