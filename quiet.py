#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webbrowser
from Foundation import NSBundle, NSObject
import rumps
import modules.google_calendar
#rumps.debug_mode(True)  # turn on command line logging information for development - default is off

class Quiet(NSObject):
    def init(self):
        self = super(Quiet, self).init()
        return self

    def run(self):
        self.app = rumps.App("Quiet", title='Q')
        self.app.menu._menu.setDelegate_(self)
        # modules
        #modules.google_calendar.start(app)
        self.google_calendar = modules.google_calendar.Module()
        self.google_calendar.start(self.app)
        # Quiet menu items
        self.app.menu.add(None) # separator
        version = NSBundle.mainBundle().infoDictionary()['CFBundleShortVersionString']
        def _about(sender):
            webbrowser.open("https://github.com/hiroshi/quiet/wiki")
        self.app.menu.add(rumps.MenuItem("quiet %s" % version, callback=_about))
        self.app.run()

    # NSMenuDelegate
    def menuWillOpen_(self, menu):
        self.google_calendar.refresh(self.app)

    # def menuDidClose_(self, menu):
    #     self.google_calendar.refresh(self.app)



if __name__ == "__main__":
    Quiet.new().run()
    # app = rumps.App("My Toolbar App", title='0')

    # print app.menu._menu
    # menu_delegate = MenuDelegate.alloc().init()
    # app.menu._menu.setDelegate_(menu_delegate)
    # print app.menu._menu.delegate()

    # app.title = "Q"
    # modules.google_calendar.start(app)
    # app.menu.add(None) # separator
    # version = NSBundle.mainBundle().infoDictionary()['CFBundleShortVersionString']
    # app.menu.add(rumps.MenuItem("quiet %s" % version, callback=about))
    # app.run()
