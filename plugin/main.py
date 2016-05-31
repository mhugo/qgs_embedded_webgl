#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from qgis.core import *
from qgis.gui import *
from PyQt4 import QtWebKit

import os
import random

class MyBridge(QObject):
    elevationsReceived = pyqtSignal("QList<int>", name='elevationsReceived')
    textureReceived = pyqtSignal("QList<int>", name='textureReceived')

    def __init__(self, iface, parent = None):
        QObject.__init__(self, parent)
        self.iface = iface

    @pyqtSlot()
    def requestElevations(self):
        print("requestElevations called")
        demLayer = None
        for lid, lyr in QgsMapLayerRegistry.instance().mapLayers().iteritems():
            if lyr.type() == QgsMapLayer.RasterLayer and lyr.rasterType() == QgsRasterLayer.GrayOrUndefined:
                demLayer = lyr
                break

        if demLayer is None:
            return

        extent = self.iface.mapCanvas().extent()
        if extent.width() > extent.height():
            h = 256
            w = int(extent.width() / extent.height() * 256.0)
        else:
            w = 256
            h = int(extent.height() / extent.width() * 256.0)
        block = demLayer.dataProvider().block(1, self.iface.mapCanvas().extent(), w, h)
        ww = 256
        hh = 256
        heightMap = [0] * ww*hh
        for x in range(ww):
            for y in range(hh):
                # FIXME why are y and x inverted relative to the texture ?
                heightMap[y*ww+x] = block.value(y, x)
        self.elevationsReceived.emit(heightMap)

    @pyqtSlot()
    def requestTexture(self):
        print("requestTexture called")
        mapSettings = self.iface.mapCanvas().mapSettings()
        job = QgsMapRendererSequentialJob(mapSettings)
        job.start()
        job.waitForFinished()
        img = job.renderedImage()
        if img.width() > img.height():
            md = img.height()
        else:
            md = img.width()
        subImg = img.copy(0, 0, md, md).scaled(256, 256)

        w = subImg.width()
        h = subImg.height()
        texture = [0] * w*h*3
        for y in xrange(h):
            for x in xrange(w):
                texture[y*w+x] = subImg.pixel(x,y)
        self.textureReceived.emit(texture)

    @pyqtSlot()
    def update(self):
        self.requestTexture()
        self.requestElevations()
        
class WebPage(QtWebKit.QWebPage):
    def javaScriptConsoleMessage(self, msg, line, source):
        print('%s line %d: %s' % (source, line, msg))

class MainPlugin:

    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction(QIcon(os.path.dirname(__file__) + "/icon.png"), \
                              u"WebGL viewer", self.iface.mainWindow())
        self.action.triggered.connect(self.run)

        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"WebGL viewer", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu(u"WebGL viewer",self.action)

    def run(self):
        print("run")
        self.webView = QtWebKit.QWebView()    
        self.webView.settings().setAttribute(QtWebKit.QWebSettings.WebGLEnabled, True)
        self.webView.settings().setAttribute(QtWebKit.QWebSettings.AcceleratedCompositingEnabled, True)
        page = WebPage()
        self.webView.setPage(page)

        self.bridge = MyBridge(self.iface)
        self.iface.mapCanvas().scaleChanged.connect(self.bridge.update)
        self.iface.mapCanvas().extentsChanged.connect(self.bridge.update)
        self.webView.page().mainFrame().addToJavaScriptWindowObject("bridge", self.bridge)

        url = QUrl.fromLocalFile(os.path.dirname(os.path.abspath(__file__)) + '/viewer.html')
        self.webView.load(url)
        self.webView.show()
        self.webView.resize(600,400)

        
                

