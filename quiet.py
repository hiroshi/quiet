#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webbrowser
from Foundation import NSBundle
import rumps
import modules.google_calendar
#rumps.debug_mode(True)  # turn on command line logging information for development - default is off

def about(sender):
    webbrowser.open("https://github.com/hiroshi/quiet/wiki")

if __name__ == "__main__":
    app = rumps.App("My Toolbar App", title='0')
    app.title = "Q"
    modules.google_calendar.start(app)
    app.menu.add(None) # separator
    version = NSBundle.mainBundle().infoDictionary()['CFBundleShortVersionString']
    app.menu.add(rumps.MenuItem("quiet %s" % version, callback=about))
    app.run()
