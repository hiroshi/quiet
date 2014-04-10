#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import sys
#sys.path.insert(0, "/Users/hiroshi/Desktop/wc/rumps") # use unicode supported fork
import rumps
import modules.google_calendar

rumps.debug_mode(True)  # turn on command line logging information for development - default is off

if __name__ == "__main__":

    app = rumps.App("My Toolbar App", title='0')
    #app.menu = [u"日本語"]
    modules.google_calendar.start(app)
    app.run()
