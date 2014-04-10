.PHONY: open, run, clean

open: dist/quiet.app
	open $<

dist/quiet.app: $(RUMPS)
	python setup.py py2app

clean:
	rm -r dist build

run: $(RUMPS)
	python quiet.py

# NOTE: At the moment, original rumps didn't support unicode characters for title, menu, etc...
RUMPS = ../rumps
export PYTHONPATH=$(RUMPS)
$(RUMPS):
	(cd .. && git checkout https://github.com/hiroshi/rumps.git)
