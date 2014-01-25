#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

import pickle
import os


class Configuration:
    def __init__(self):
        self.configuration = {}
        self.confFile = ".configuration"

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
            f = open(self.confFile)
            self.configuration = pickle.load(f)
            f.close()
        else:
            self.setDefaults()

    def storeConfiguration(self):
        """Store configuration into file to make them persistent"""
        f = open(self.confFile, "w+")
        pickle.dump(self.configuration, f)
        f.close()
