#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

from category import CategoryContainer
from todolist import TodoListContainer
from configuration import Configuration
from activity import Activities
from stats import Stats
from collections import Iterable
import time, os

class Waktu(object):
    """Main class of Waktu project"""

    def __init__(self):
        self.categories = CategoryContainer()
        self.todolist = TodoListContainer()
        self.stats = Stats()
        self.configuration = Configuration()
        self.activities = Activities()

    def getCategories(self):
        return self.categories

    def getTodolist(self):
        return self.todolist

    def getStats(self):
        return self.stats

    def getConfiguration(self):
        return self.configuration

    def getActivities(self):
        return self.activities

    def restoreCategories(self):
        """Restore stored categories"""
        self.getCategories().restoreCategories()

    def storeCategories(self):
        """Store categories into file to make them persistent"""
        self.getCategories().storeCategories()

    def restoreTodolist(self):
        """Restore stored todolist"""
        self.getTodolist().restoreTodolist()

    def storeTodolist(self):
        """Store todolist into file to make them persistent"""
        self.getTodolist().storeTodolist()

    def restoreConfiguration(self):
        """Restore stored configuration"""
        self.getConfiguration().restoreConfiguration()

    def storeConfiguration(self):
        """Store configuration into file to make them persistent"""
        self.getConfiguration().storeConfiguration()

    def restoreStats(self, _date = time.strftime("%Y%m%d")):
        """Restore stored stats to the day if there are any"""
        self.getStats().updateRecords(_date)

    def storeStats(self, _date = time.strftime("%Y%m%d")):
        """Store stats into file to make them persistent"""
        self.getStats().storeRecords(_date)

    def restoreActivities(self):
        """Restore stored activities"""
        self.getActivities().restoreActivities()

    def storeActivities(self):
        """Store activities into file to make them persistent"""
        self.getActivities().storeActivities()

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
            os.remove('stats/'+statFile)

        self.getCategories().clearCategories()
        self.getTodolist().clearTodolist()
        self.getStats().clearStats()
        self.restoreConfiguration()
        self.getActivities().clearActivities()
