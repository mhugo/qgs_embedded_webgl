#!/usr/bin/env python
# -*- coding: utf-8 -*-
def name():
    return "WebGL viewer"
def description():
    return "WebGL viewer"
def version():
    return "Version 1.0"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "2.14"
def qgisMaximumVersion():
    return "2.99"
def classFactory(iface):
    from main import MainPlugin
    return MainPlugin(iface)
