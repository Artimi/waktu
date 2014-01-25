#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

import pickle
import os


class Activity:
    def __init__(self, name='', pid=0):
        self.name = name
        self.pid = pid


class Activities:
    def __init__(self):
        self.activities = set()
        self.activitiesFile = ".activities"

    def __iter__(self):
        return iter(self.activities)

    def add(self, activity):
        """Add _activity to the set. Automatically skip
        already added activities"""
        self.activities.add(activity)

    def restore(self):
        """Restore stored activities"""
        if os.path.exists(self.activitiesFile):
            f = open(self.activitiesFile)
            self.activities = pickle.load(f)
            f.close()

    def store(self):
        """Store activities into file to make them persistent"""
        f = open(self.activitiesFile, "w+")
        pickle.dump(self.activities, f)
        f.close()

    def clear(self):
        self.activities = set()
