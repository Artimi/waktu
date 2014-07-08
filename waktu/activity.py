#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

import os
import json


class Activity(object):
    """This class encapsulate information about individual Activity.
    If pid is provided class will search for process information"""
    def __init__(self, title='', pid=0, name='', cmdline='', exe=''):
        self.title = title
        self.pid = pid
        self.name = name
        self.cmdline = cmdline
        self.exe = exe
        if self.pid != 0:
            self.name = self._get_process_info('comm')
            self.cmdline = self._get_process_info('cmdline')
            self.exe = os.path.realpath('/proc/' + str(self.pid) + '/exe')

    @property
    def key(self):
        """ID representing given Activity"""
        return self.name + '-' + self.title

    def get_content(self):
        """Serves for storage."""
        return {'name': self.name,
                'title': self.title,
                'cmdline': self.cmdline,
                'exe': self.cmdline}

    def _get_process_info(self, info):
        """Reads information of process like name of process and command line
        arguments."""
        with open('/proc/' + str(self.pid) + '/' + info) as f:
            return f.read().replace('\x00', ' ').strip()


class Activities(object):
    """This is container of Activity objects. Activity are stored in dict
    with key compounded of name and title."""
    def __init__(self, activities_file):
        self.activities = dict()
        self.activities_file = activities_file

    def __iter__(self):
        """Iterate over values only"""
        for value in self.activities.itervalues():
            yield value

    def __len__(self):
        return len(self.activities)

    def add(self, activity):
        """Add Activity to the dictionary. Overwrite already added activity
        with same key"""
        self.activities[activity.key] = activity

    def restore(self):
        """Restore stored activities"""
        if os.path.exists(self.activities_file):
            self.clear()
            with open(self.activities_file) as f:
                file_content = json.load(f)
            for activity in file_content:
                self.add(Activity(title=activity['title'],
                                  name=activity['name'],
                                  cmdline=activity['cmdline'],
                                  exe=activity['exe']))

    def store(self):
        """Store activities into file to make them persistent"""
        with open(self.activities_file, "w+") as f:
            json.dump(self.get_content(), f, indent=1)

    def clear(self):
        self.activities.clear()

    def get_content(self):
        """Serves for storage."""
        return [activity.get_content() for activity in self.activities.itervalues()]
