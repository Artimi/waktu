#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

import os
import json


class Activity(object):
    def __init__(self, name='', pid=0):
        self.name = name
        self.pid = pid

    def getContent(self):
        return {'name': self.name, 'pid': self.pid}


class Activities(object):
    def __init__(self, activitiesFile):
        self.activities = set()
        self.activitiesFile = activitiesFile

    def __iter__(self):
        return iter(self.activities)

    def __len__(self):
        return len(self.activities)

    def add(self, activity):
        """Add _activity to the set. Automatically skip
        already added activities"""
        self.activities.add(activity)

    def restore(self):
        """Restore stored activities"""
        if os.path.exists(self.activitiesFile):
            self.clear()
            with open(self.activitiesFile) as f:
                file_content = json.load(f)
            for activity in file_content:
                self.add(Activity(activity['name'], activity['pid']))

    def store(self):
        """Store activities into file to make them persistent"""
        with open(self.activitiesFile, "w+") as f:
            json.dump(self.get_content(), f, indent=1)

    def clear(self):
        self.activities.clear()

    def get_content(self):
        return [activity.get_content() for activity in self.activities]
