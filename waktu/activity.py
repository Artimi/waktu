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
            with open(self.activitiesFile) as f:
                self.activities = pickle.load(f)

    def store(self):
        """Store activities into file to make them persistent"""
        with open(self.activitiesFile, "w+") as f:
            pickle.dump(self.activities, f)

    def clear(self):
        self.activities = set()
