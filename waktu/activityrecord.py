#-*- coding: UTF-8 -*-
"""
Waktu module for object related to activity records. An ActivityRecord
in Waktu's context means an record of an activity, a category which
the activity belongs to, a start time of the recorded interval and its
end. It's used for statictics.
"""

from activity import Activity
from time import time


class ActivityRecord(object):
    """Contains record about every activity"""

    def __init__(self, category='', activity=Activity(), start_time=time(), end_time=time()):
        self.category = category
        self.activity = activity
        self.start_time = start_time
        self.end_time = end_time

    def get_content(self):
        return {'category': self.category,
                'activity': self.activity.get_content(),
                'startTime': self.start_time,
                'endTime': self.end_time}
