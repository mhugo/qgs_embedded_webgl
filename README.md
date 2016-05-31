Embedded WebGL for QGIS
=======================

This is a proof of concept to experiment the embedding of a WebGL window in QGIS.

Rationale: be able to use an existing WebGL / javascript based framework (like iTowns) to view 3D GIS data.

Qt versions
-----------

Part of the experiment was to test whether QtWebKit is usable as a web engine for existing webgl frameworks.

Cesium does not seem to work with it.

iTowns had a bug that prevents it to work (https://github.com/iTowns/itowns2/issues/75).

* Qt will replace webkit by QtWebEngine in the long term.
* QtWebEngine is introduced starting with QT 5.4
* Qt won't make QtWebKit obsolete before Qt 6
* Debian stretch removed QtWebKit from Qt4

This leads us to use QtWebKit on a Qt5 compilation of QGIS. And see in the future if we need to use QtWebEngine.

Data streaming
--------------

A QGIS plugin starts a QtWebKit that embeds a three.js scene.

Data from QGIS (texture and DEM for now) are sent to the three.js scene thanks to the "QtWebkit bridge" provided.

It works, but performances may be limited.

Data are passed by using lists (QList of int and arrays in javascript). This could be improved by de/serializing to strings.

Pan / Zoom from the QGIS canvas update the WebGL scene.

