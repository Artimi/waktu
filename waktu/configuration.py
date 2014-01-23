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
        self.setValue("mode", 0)
        self.setValue("state", 1)
        self.storeConfiguration()
    
    def getValue(self, _option):
        """Get the value of the option _option"""
        return self.configuration[_option]
    
    def setValue(self, _option, _value):
        """Set the option _option to the value _value"""
        self.configuration[_option] = _value
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
        
