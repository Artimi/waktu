#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

from gi.repository import Wnck, Gdk, GObject, Notify, GLib
from activityrecord import ActivityRecord
from threading import Thread, Event
from time import sleep, time
import copy


class TimeTracker(Thread):
    """Core module of this project. It's running in separated thread
    to not block GUI."""
    stopthread = Event()
    track = Event()
    mode = Event()

    def __init__(self, stat, categories, activities, configuration):
        Thread.__init__(self)
        self.categories = categories
        self.activities = activities
        self.stat = stat
        self.lastActivity = ActivityRecord()
        self.screen = Wnck.Screen.get_default()
        self.n = Notify.Notification()
        self.tmpName = ''

        if configuration.getValue('state'):
            self.track.set()
        else:
            self.track.clear()

        if configuration.getValue('mode'):
            self.mode.set()
        else:
            self.mode.clear()

    def run(self):
        """Start tracking user activities"""

        while not self.stopthread.isSet():
            sleep(1)

            """Skip tracking if it's disabled"""
            if not self.track.isSet():
                continue

            Gdk.threads_enter()
            GObject.idle_add(self.screen.force_update)
            active_window = self.screen.get_active_window()

            """Skip if there is no active window"""
            if active_window is None:
                Gdk.threads_leave()
                continue

            appName = active_window.get_application().get_name()
            appPid = active_window.get_application().get_pid()

            """If the learning mode is activive, only append an activity"""
            if self.mode.isSet():
                self.activities.addActivity(appName)
                Gdk.threads_leave()
                continue

            if self.lastActivity.activity.pid == appPid:
                """Still the same activity, just actualize the end time"""
                self.lastActivity.endTime = time()

            else:
                """New activity, actualize the lastActivity and append
                the new activity"""
                if self.lastActivity.activity.pid != 0:
                    tmp = copy.deepcopy(self.lastActivity)
                    self.stat.appendActivityRecord(tmp)
                    self.activities.addActivity(tmp.activity.name)
                    print "DBG: Zmena aktivity! Ulozena aktivita %s (%s)" % (tmp.activity.name, tmp.category)

                self.lastActivity.activity.name = appName
                self.lastActivity.activity.pid = appPid
                self.lastActivity.category = 'OTHER'
                self.getCorrectCategory()
                self.lastActivity.startTime = time()
                self.lastActivity.endTime = time()

            Gdk.threads_leave()

        if self.track.isSet() and not self.mode.isSet():
            tmp = copy.deepcopy(self.lastActivity)
            self.stat.appendActivityRecord(tmp)
            print "DBG: Ulozena aktivita %s (%s)" % (tmp.activity.name, tmp.category)

        """Store all records to file to make them persistent"""
        self.stat.storeRecords()
        self.activities.store()

    def stop(self):
        """Stop the tracking system, uses id stored in initialization"""
        self.stopthread.set()

    def getCorrectCategory(self, activity=None):
        """Find out category where the activity belongs to"""
        if activity is None:
            activity = self.lastActivity.activity

        activityCategories = self.categories.getContainingCategories(activity)
        if len(activityCategories) == 0:
            """The activity isn't in any category"""
            self.lastActivity.category = 'OTHER'
        elif len(activityCategories) == 1:
            """The activity is in exactly one category"""
            self.lastActivity.category = activityCategories[0].name
        else:
            """The activity is in more than one category.
            The Waktu needs to ask user."""
            lastOccurrence = self.stat.getLastOccurrence(activity.name)
            # 10 minutes is the default time to remember users choice
            if lastOccurrence is None or (time() - lastOccurrence.endTime) > 600:
                self.askUser(activity, activityCategories)
            else:
                self.lastActivity.category = lastOccurrence.category

    def askUser(self, activity, categories):
        """Creates a notification and asks a user where the activity belongs to"""
        if not Notify.is_initted():
            Notify.init('Waktu')

        self.n.clear_hints()
        self.n.clear_actions()
        self.n.set_property('summary', 'Kam patří aktivita %s?' % activity.name)
        self.n.set_property('body', 'Zdá se, že tuto aktivitu máte zvolenou ve více kategoriích. Zvolte, prosím, níže jednu, do které spadá tato aktivita práve teď.')
        self.n.set_property('icon_name', 'dialog-question')
        self.n.set_urgency(Notify.Urgency.NORMAL)
        self.n.set_timeout(Notify.EXPIRES_NEVER)
        self.n.set_hint("resident", GLib.Variant('b', True))

        for cat in categories:
            self.n.add_action(cat.name, cat.name, self.getUserAnswer, activity, None)

        self.n.add_action("OTHER", "Jinam", self.getUserAnswer, activity, None)

        self.n.show()

    def getUserAnswer(self, n, action, data):
        """Process user answer and delegate result"""
        n.close()

        if self.lastActivity.activity.name == data.name:
            """The focused app is still the same"""
            self.lastActivity.category = action
        else:
            """There is another activity, need to find it backwards"""
            self.stat.getLastOccurrence(data.name).category = action
