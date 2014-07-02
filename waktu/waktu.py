#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

from category import CategoryContainer
from configuration import Configuration
from activity import Activities
from stats import Stats
import time
import os


class Waktu(object):
    """Main class of Waktu project"""

    def __init__(self):
        self.setConfigPaths()
        self.categories = CategoryContainer(self.configPath['categories'])
        self.stats = Stats(self.configPath['stats'])
        self.configuration = Configuration(self.configPath['configuration'])
        self.activities = Activities(self.configPath['activities'])

    def setConfigPaths(self):
        self.configDir = os.path.expanduser("~/.config/waktu/")
        if not os.path.isdir(self.configDir):
            os.mkdir(self.configDir)
        self.configPath = {
            'categories': self.configDir + 'categories.json',
            'activities': self.configDir + 'activities.json',
            'configuration': self.configDir + 'configuration.json',
            'stats': self.configDir + 'stats/'
        }
        if not os.path.isdir(self.configPath['stats']):
            os.mkdir(self.configPath['stats'])

    def restoreCategories(self):
        """Restore stored categories"""
        self.categories.restore()

    def storeCategories(self):
        """Store categories into file to make them persistent"""
        self.categories.store()

    def restoreConfiguration(self):
        """Restore stored configuration"""
        self.configuration.restore()

    def storeConfiguration(self):
        """Store configuration into file to make them persistent"""
        self.configuration.store()

    def restoreStats(self, dat=time.strftime("%Y%m%d")):
        """Restore stored stats to the day if there are any"""
        self.stats.restore(dat)

    def storeStats(self, dat=time.strftime("%Y%m%d")):
        """Store stats into file to make them persistent"""
        self.stats.store(dat)

    def restoreActivities(self):
        """Restore stored activities"""
        self.activities.restore()

    def storeActivities(self):
        """Store activities into file to make them persistent"""
        self.activities.store()

    def clearAllData(self):
        """Clear all user created data"""
        if os.path.exists('.categories.json'):
            os.remove('.categories.json')
        if os.path.exists('.activities.json'):
            os.remove('.activities.json')
        if os.path.exists('.configuration.json'):
            os.remove('.configuration.json')

        for statFile in os.listdir('stats'):
            os.remove('stats/' + statFile)

        self.categories.clearCategories()
        self.stats.clearStats()
        self.restoreConfiguration()
        self.activities.clear()
