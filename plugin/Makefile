# global

PLUGINNAME = webgl_viewer

PY_FILES = main.py __init__.py

EXTRAS = metadata.txt icon.png js three.js viewer.html

UI_FILES =

VERSION=$(shell grep "version=" metadata.txt | cut -d'=' -f 2)

%.qm : %.ts
	lrelease $<

# The deploy  target only works on unix like operating system where
# the Python plugin directory is located at:
# $HOME/.qgis2/python/plugins
deploy: transcompile
	mkdir -p $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	cp -vf $(PY_FILES) $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	#cp -vf $(UI_FILES) $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)
	cp --parents -vfRa $(EXTRAS) $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)

# The dclean target removes compiled python files from plugin directory
# also delets any .svn entry
dclean:
	find $(HOME)/.qgis2/python/plugins/$(PLUGINNAME) -iname "*.pyc" -delete
	find $(HOME)/.qgis2/python/plugins/$(PLUGINNAME) -iname ".svn" -prune -exec rm -Rf {} \;

# The derase deletes deployed plugin
derase:
	rm -Rf $(HOME)/.qgis2/python/plugins/$(PLUGINNAME)

# The zip target deploys the plugin and creates a zip file with the deployed
# content. You can then upload the zip file on http://plugins.qgis.org
zip: deploy dclean
	echo $(VERSION)
	rm -f $(PLUGINNAME)*.zip
	cd $(HOME)/.qgis2/python/plugins; zip -9r $(CURDIR)/$(PLUGINNAME)-$(VERSION).zip $(PLUGINNAME)

# transup
# update .ts translation files
transup:
	pylupdate4 Makefile

# transcompile
# compile translation files into .qm binary format
transcompile: $(TRANSLATIONS:.ts=.qm)

# transclean
# deletes all .qm files
transclean:
	rm -f i18n/*.qm

clean:
	rm $(UI_FILES) $(RESOURCE_FILES)

