#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

from collections import deque
import json
import os
import time


class Stats(object):
    """Statistics class, handles records of an array"""
    def __init__(self, statsDir):
        self.activityRecords = deque()
        self.statsDir = statsDir

    def __len__(self):
        return len(self.activityRecords)

    def appendActivityRecord(self, activityRecord):
        self.activityRecords.append(activityRecord)

    def lastActivityRecord(self):
        return self.activityRecords[-1]

    def getLastOccurrence(self, activityName):
        """Return the last occurrence of an activityRecord by given name"""
        for ar in reversed(self.activityRecords):
            if ar.activity.name == activityName:
                return ar
        return None

    def restore(self, date=time.strftime("%Y%m%d")):
        """Open data file with stats and update records"""
        filename = self.statsDir + date + '.json'
        if os.path.exists(filename):
            with open(filename) as f:
                self.activityRecords = deque(json.load(f))
            return True
        else:
            return False

    def store(self, date=time.strftime("%Y%m%d")):
        """Store the activityRecords structure into file"""
        filename = self.statsDir + date + '.json'
        with open(filename, 'w+') as f:
            json.dump(self.get_content(), f)

    def get_pie_summary(self):
        pie_summary = {}
        pie_summary['categories'] = []
        pie_summary['values'] = []
        for ar in self.activityRecords:
            if ar.category not in pie_summary['categories']:
                pie_summary['categories'].append(unicode(ar.category, errors='ignore'))
                pie_summary['values'].append(ar.endTime - ar.startTime)
            else:
                index = pie_summary['categories'].index(ar.category)
                pie_summary['values'][index] += ar.endTime - ar.startTime
        return pie_summary

    def clearStats(self):
        self.activityRecords = deque()

    def get_content(self):
        return [activityRecord.get_content() for activityRecord in self.activityRecords]
