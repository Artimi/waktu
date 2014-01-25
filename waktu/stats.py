#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

from collections import deque
import pickle
import os
import time


class Stats:
    """Statistics class, handles records of an array"""
    def __init__(self):
        self.activityRecords = deque()

    def appendActivityRecord(self, activityRecord):
        self.activityRecords.append(activityRecord)

    def lastActivityRecord(self):
        return self.activityRecords[-1]

    def getLastOccurrence(self, activityName):
        """Return the last occurrence of an activityRecord by given name"""
        for ar in reversed(self.activityRecords):
            if ar.getActivity().getName() == activityName:
                return ar
        return None

    def updateRecords(self, date=time.strftime("%Y%m%d")):
        """Open data file with stats and update records"""
        filename = 'stats/' + date + '.dat'
        if os.path.exists(filename):
            f = open(filename)
            self.activityRecords = pickle.load(f)
            f.close()
            return True
        else:
            return False

    def storeRecords(self, date=time.strftime("%Y%m%d")):
        """Store the activityRecords structure into file"""
        filename = 'stats/' + date + '.dat'
        f = open(filename, 'w+')
        pickle.dump(self.activityRecords, f)
        f.close()

    def get_pie_summary(self):
        pie_summary = {}
        pie_summary['categories'] = []
        pie_summary['values'] = []
        for ar in self.activityRecords:
            if ar.getCategory() not in pie_summary['categories']:
                pie_summary['categories'].append(unicode(ar.getCategory(), errors='ignore'))
                pie_summary['values'].append(ar.getEndTime() - ar.getStartTime())
            else:
                index = pie_summary['categories'].index(ar.getCategory())
                pie_summary['values'][index] += ar.getEndTime() - ar.getStartTime()
        return pie_summary

    def clearStats(self):
        self.activityRecords = deque()
