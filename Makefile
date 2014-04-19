RUMPS = ../rumps
export PYTHONPATH=$(RUMPS)
export VERSION=0.1.0

.PHONY: all
all: dist/quiet-$(VERSION).zip
dist/quiet-$(VERSION).zip: dist/quiet.app
	(cd dist && zip -r $(notdir $@) $(notdir $^))

.PHONY: open
open: dist/quiet.app
	open $<

.PHONY: app
app: dist/quiet.app
dist/quiet.app: $(RUMPS)
	python setup.py py2app

.PHONY: clean
clean:
	rm -rf dist build

.PHONY: run
run: $(RUMPS)
	python quiet.py

# NOTE: At the moment, original rumps didn't support unicode characters for title, menu, etc...
$(RUMPS):
	(cd .. && git checkout https://github.com/hiroshi/rumps.git)
