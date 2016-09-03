#!/usr/bin/env python
# encoding: utf-8
# cocoa_keypress_monitor.py
# Copyright © 2016 Bjarte Johansen <Bjarte.Johansen@gmail.com>
#
# The MIT License (MIT)
#

from .generic import Catcher as GenericCatcher


class Catcher(GenericCatcher):

    def __init__(self, *args, **kwargs):
        super(Catcher, self).__init__(*args, **kwargs)

    def run(self):

        from AppKit import NSApplication, NSApp
        from Foundation import NSObject, NSLog
        from Cocoa import NSEvent, NSKeyDownMask
        from PyObjCTools import AppHelper

        def handler(event):
            try:
                character = event.keyCode()
                self.callback(character, "apple-keycode")

            except KeyboardInterrupt:
                AppHelper.stopEventLoop()

        class AppDelegate(NSObject):
            def applicationDidFinishLaunching_(self, notification):
                mask = NSKeyDownMask
                NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask, handler)

        app = NSApplication.sharedApplication()
        delegate = AppDelegate.alloc().init()
        NSApp().setDelegate_(delegate)
        AppHelper.runEventLoop()

