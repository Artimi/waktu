#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

from category import CategoryContainer
from todolist import TodoListContainer
from configuration import Configuration
from activity import Activities
from stats import Stats
import time
import os


class Waktu(object):
    """Main class of Waktu project"""

    def __init__(self):
        self.categories = CategoryContainer()
        self.todolist = TodoListContainer()
        self.stats = Stats()
        self.configuration = Configuration()
        self.activities = Activities()

    def restoreCategories(self):
        """Restore stored categories"""
        self.categories.restoreCategories()

    def storeCategories(self):
        """Store categories into file to make them persistent"""
        self.categories.storeCategories()

    def restoreTodolist(self):
        """Restore stored todolist"""
        self.todolist.restoreTodolist()

    def storeTodolist(self):
        """Store todolist into file to make them persistent"""
        self.todolist.storeTodolist()

    def restoreConfiguration(self):
        """Restore stored configuration"""
        self.configuration.restoreConfiguration()

    def storeConfiguration(self):
        """Store configuration into file to make them persistent"""
        self.configuration.storeConfiguration()

    def restoreStats(self, dat=time.strftime("%Y%m%d")):
        """Restore stored stats to the day if there are any"""
        self.stats.updateRecords(dat)

    def storeStats(self, dat=time.strftime("%Y%m%d")):
        """Store stats into file to make them persistent"""
        self.stats.storeRecords(dat)

    def restoreActivities(self):
        """Restore stored activities"""
        self.activities.restore()

    def storeActivities(self):
        """Store activities into file to make them persistent"""
        self.activities.store()

    def clearAllData(self):
        """Clear all user created data"""
        if os.path.exists('.categories.tree'):
            os.remove('.categories.tree')
        if os.path.exists('.activities'):
            os.remove('.activities')
        if os.path.exists('.configuration'):
            os.remove('.configuration')
        if os.path.exists('.todolist.tree'):
            os.remove('.todolist.tree')

        for statFile in os.listdir('stats'):
            os.remove('stats/' + statFile)

        self.categories.clearCategories()
        self.todolist.clearTodolist()
        self.stats.clearStats()
        self.restoreConfiguration()
        self.activities.clear()
