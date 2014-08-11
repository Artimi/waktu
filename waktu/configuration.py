#-*- coding: UTF-8 -*-
"""
Waktu module for configuration related object. Handles Waktu's configuration, its storing and restoring.
"""
import json
import os


class Configuration(object):
    def __init__(self, conf_file):
        self.configuration = {}
        self.conf_file = conf_file

    def set_defaults(self):
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
        self.set_defaults()
        if os.path.exists(self.conf_file):
            with open(self.conf_file) as f:
                file_content = json.load(f)
            for key, value in file_content.iteritems():
                self.configuration[key] = value

    def store(self):
        """Store configuration into file to make them persistent"""
        with open(self.conf_file, 'w+') as f:
            json.dump(self.configuration, f, indent=1)
