#-*- coding: UTF-8 -*-
"""
"""
from collections import deque
import json
import os
import time


class Stats(object):
    """Statistics class, handles records of an array"""
    def __init__(self, stats_dir):
        self.activity_records = deque()
        self.stats_dir = stats_dir

    def __len__(self):
        return len(self.activity_records)

    def append(self, activity_record):
        self.activity_records.append(activity_record)

    def get_last_occurrence(self, activity_name):
        """Return the last occurrence of an activityRecord by given name"""
        for ar in reversed(self.activity_records):
            if ar.activity.name == activity_name:
                return ar
        return None

    def restore(self, date=time.strftime("%Y%m%d")):
        """Open data file with stats and update records"""
        filename = self.stats_dir + date + '.json'
        if os.path.exists(filename):
            with open(filename) as f:
                self.activity_records = deque(json.load(f))
            return True
        else:
            return False

    def store(self, date=time.strftime("%Y%m%d")):
        """Store the activityRecords structure into file"""
        filename = self.stats_dir + date + '.json'
        with open(filename, 'w+') as f:
            json.dump(self.get_content(), f)

    def get_pie_summary(self):
        pie_summary = dict()
        pie_summary['categories'] = []
        pie_summary['values'] = []
        #for ar in self.activity_records:
        #    if ar.category not in pie_summary['categories']:
        #        pie_summary['categories'].append(unicode(ar.category, errors='ignore'))
        #        pie_summary['values'].append(ar.end_time - ar.start_time)
        #    else:
        #        index = pie_summary['categories'].index(ar.category)
        #        pie_summary['values'][index] += ar.end_time - ar.start_time
        return pie_summary

    def clear(self):
        self.activity_records = deque()

    def get_content(self):
        return [activityRecord.get_content() for activityRecord in self.activity_records]
