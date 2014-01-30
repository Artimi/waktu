#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

import pickle
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
        self.storeConfiguration()

    def __getitem__(self, option):
        """Get the value of the option"""
        return self.configuration[option]

    def __setitem__(self, option, value):
        """Set the option to the value"""
        self.configuration[option] = value
        self.storeConfiguration()

    def restoreConfiguration(self):
        """Restore stored configuration"""
        if os.path.exists(self.confFile):
            with open(self.confFile) as f:
                self.configuration = pickle.load(f)
        else:
            self.setDefaults()

    def storeConfiguration(self):
        """Store configuration into file to make them persistent"""
        with open(self.confFile, "w+") as f:
            pickle.dump(self.configuration, f)
