#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

import json
import os


class Configuration(object):
    def __init__(self, confFile):
        self.configuration = {}
        self.confFile = confFile

    def setDefaults(self):
        """Set the default configuration in case there is
        no configuration set already"""
        self["mode"] = 0
        self["state"] = 1
        self.store()

    def __getitem__(self, option):
        """Get the value of the option"""
        return self.configuration[option]

    def __setitem__(self, option, value):
        """Set the option to the value"""
        self.configuration[option] = value
        self.store()

    def restore(self):
        """Restore stored configuration"""
        self.setDefaults()
        if os.path.exists(self.confFile):
            with open(self.confFile) as f:
                file_content = json.load(f)
            for key, value in file_content.iteritems():
                self.configuration[key] = value

    def store(self):
        """Store configuration into file to make them persistent"""
        with open(self.confFile, 'w+') as f:
            json.dump(self.configuration, f, indent=1)
