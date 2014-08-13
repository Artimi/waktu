#-*- coding: UTF-8 -*-
"""
Waktu main module containing a Controller. Controller is designed to be
a heart of the whole application.
"""
from category import CategoryContainer
from configuration import Configuration
from activity import Activities
from stats import Stats
import time
import os


class Controller(object):
    """Main class of Waktu project"""

    def __init__(self):
        self.set_config_paths()
        self.categories = CategoryContainer(self.config_path['categories'])
        self.stats = Stats(self.config_path['stats'])
        self.configuration = Configuration(self.config_path['configuration'])
        self.activities = Activities(self.config_path['activities'])

    def set_config_paths(self):
        self.config_dir = os.path.expanduser("~/.config/waktu/")
        if not os.path.isdir(self.config_dir):
            os.mkdir(self.config_dir)
        self.config_path = {
            'categories': self.config_dir + 'categories.json',
            'activities': self.config_dir + 'activities.json',
            'configuration': self.config_dir + 'configuration.json',
            'stats': self.config_dir + 'stats/'
        }
        if not os.path.isdir(self.config_path['stats']):
            os.mkdir(self.config_path['stats'])

    def restore_categories(self):
        """Restore stored categories"""
        self.categories.restore()

    def store_categories(self):
        """Store categories into file to make them persistent"""
        self.categories.store()

    def restore_configuration(self):
        """Restore stored configuration"""
        self.configuration.restore()

    def store_configuration(self):
        """Store configuration into file to make them persistent"""
        self.configuration.store()

    def restore_stats(self, dat=time.strftime("%Y%m%d")):
        """Restore stored stats to the day if there are any"""
        self.stats.restore(dat)

    def store_stats(self, dat=time.strftime("%Y%m%d")):
        """Store stats into file to make them persistent"""
        self.stats.store(dat)

    def restore_activites(self):
        """Restore stored activities"""
        self.activities.restore()

    def store_activities(self):
        """Store activities into file to make them persistent"""
        self.activities.store()

    def clear_all(self):
        """Clear all user created data"""
        if os.path.exists(self.config_dir + 'categories.json'):
            os.remove(self.config_dir + 'categories.json')
        if os.path.exists(self.config_dir + 'activities.json'):
            os.remove(self.config_dir + 'activities.json')
        if os.path.exists(self.config_dir + 'configuration.json'):
            os.remove(self.config_dir + 'configuration.json')

        for statFile in os.listdir(self.config_dir + 'stats'):
            os.remove(self.config_dir + 'stats/' + statFile)

        self.categories.clear()
        self.stats.clear()
        self.restore_configuration()
        self.activities.clear()
