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
               
    def appendActivityRecord(self, _activityRecord):
        self.activityRecords.append(_activityRecord)
        
    def lastActivityRecord(self):
        return self.activityRecords[-1]
        
    def getLastOccurrence(self, _activityName):
        """Return the last occurrence of an activityRecord by given name"""
        for ar in reversed(self.activityRecords):
            if ar.getActivity().getName() == _activityName:
                return ar
        return None
        
    def updateRecords(self, _date=time.strftime("%Y%m%d")):
        """Open data file with stats and update records"""
        _filename = 'stats/' + _date + '.dat'
        if os.path.exists(_filename):
            f = open(_filename)
            self.activityRecords = pickle.load(f)
            f.close()
            return True
        else:
            return False
            
    def storeRecords(self, _date=time.strftime("%Y%m%d")):
        """Store the activityRecords structure into file"""
        _filename = 'stats/' + _date + '.dat'
        f = open(_filename,'w+')
        pickle.dump(self.activityRecords,f)
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
