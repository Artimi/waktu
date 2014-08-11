#-*- coding: UTF-8 -*-
"""
"""
import os
import json


class Activity(object):
    def __init__(self, name='', pid=0):
        self.name = name
        self.pid = pid

    def get_content(self):
        return {'name': self.name, 'pid': self.pid}


class Activities(object):
    def __init__(self, activities_file):
        self.activities = set()
        self.activities_file = activities_file

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
        if os.path.exists(self.activities_file):
            self.clear()
            with open(self.activities_file) as f:
                file_content = json.load(f)
            for activity in file_content:
                self.add(Activity(activity['name'], activity['pid']))

    def store(self):
        """Store activities into file to make them persistent"""
        with open(self.activities_file, "w+") as f:
            json.dump(self.get_content(), f, indent=1)

    def clear(self):
        self.activities.clear()

    def get_content(self):
        return [activity.get_content() for activity in self.activities]
