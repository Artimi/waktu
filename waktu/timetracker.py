#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

from category import Category
from gi.repository import Wnck, Gdk, Gtk, GObject, Notify, GLib
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

    def __init__(self, _stat, _categories, _activities, _configuration):
        Thread.__init__(self)
        self.categories = _categories
        self.activities = _activities
        self.stat = _stat
        self.lastActivity = ActivityRecord()
        self.screen = Wnck.Screen.get_default()
        self.n = Notify.Notification()
        self.tmpName = ''

        if _configuration.getValue('state'):
            self.track.set()
        else:
            self.track.clear()

        if _configuration.getValue('mode'):
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
            if active_window == None:
                Gdk.threads_leave()
                continue

            appName = active_window.get_application().get_name()
            appPid = active_window.get_application().get_pid()

            """If the learning mode is activive, only append an activity"""
            if self.mode.isSet():
                self.activities.addActivity(appName)
                Gdk.threads_leave()
                continue

            if self.lastActivity.getActivity().getPid() == appPid:
                """Still the same activity, just actualize the end time"""
                self.lastActivity.setEndTime(time())

            else:
                """New activity, actualize the lastActivity and append
                the new activity"""
                if self.lastActivity.getActivity().getPid() != 0:
                    tmp = copy.deepcopy(self.lastActivity)
                    self.stat.appendActivityRecord(tmp)
                    self.activities.addActivity(tmp.getActivity().getName())
                    print "DBG: Zmena aktivity! Ulozena aktivita %s (%s)" % (tmp.getActivity().getName(), tmp.getCategory())

                self.lastActivity.getActivity().setName(appName)
                self.lastActivity.getActivity().setPid(appPid)
                self.lastActivity.setCategory('OTHER')
                self.getCorrectCategory()
                self.lastActivity.setStartTime(time())
                self.lastActivity.setEndTime(time())

            Gdk.threads_leave()

        if self.track.isSet() and not self.mode.isSet():
            tmp = copy.deepcopy(self.lastActivity)
            self.stat.appendActivityRecord(tmp)
            print "DBG: Ulozena aktivita %s (%s)" % (tmp.getActivity().getName(), tmp.getCategory())

        """Store all records to file to make them persistent"""
        self.stat.storeRecords()
        self.activities.storeActivities()

    def stop(self):
        """Stop the tracking system, uses id stored in initialization"""
        self.stopthread.set()

    def getCorrectCategory(self, _activity = None):
        """Find out category where the activity belongs to"""
        if _activity == None:
            _activity = self.lastActivity.getActivity()

        activityCategories = self.categories.getContainingCategories(_activity)
        if len(activityCategories) == 0:
            """The activity isn't in any category"""
            self.lastActivity.setCategory('OTHER')
        elif len(activityCategories) == 1:
            """The activity is in exactly one category"""
            self.lastActivity.setCategory(activityCategories[0].name)
        else:
            """The activity is in more than one category.
            The Waktu needs to ask user."""
            lastOccurrence = self.stat.getLastOccurrence(_activity.getName())
            if lastOccurrence == None or (time() - lastOccurrence.getEndTime()) > 600 : # 10 minutes is the default time to remember users choice
                self.askUser(_activity, activityCategories)
            else:
                self.lastActivity.setCategory(lastOccurrence.getCategory())

    def askUser(self, _activity, _categories):
        """Creates a notification and asks a user where the activity belongs to"""
        if not Notify.is_initted():
            Notify.init('Waktu')

        self.n.clear_hints()
        self.n.clear_actions()
        self.n.set_property('summary','Kam patří aktivita %s?' % _activity.getName())
        self.n.set_property('body', 'Zdá se, že tuto aktivitu máte zvolenou ve více kategoriích. Zvolte, prosím, níže jednu, do které spadá tato aktivita práve teď.')
        self.n.set_property('icon_name','dialog-question')
        self.n.set_urgency(Notify.Urgency.NORMAL)
        self.n.set_timeout(Notify.EXPIRES_NEVER)
        self.n.set_hint("resident", GLib.Variant('b',True))

        for cat in _categories:
            self.n.add_action(cat.name, cat.name, self.getUserAnswer, _activity, None)

        self.n.add_action("OTHER", "Jinam", self.getUserAnswer, _activity, None)

        self.n.show()

    def getUserAnswer(self, n, _action, _data):
        """Process user answer and delegate result"""
        n.close()

        if self.lastActivity.getActivity().getName() == _data.getName():
            """The focused app is still the same"""
            self.lastActivity.setCategory(_action)
        else:
            """There is another activity, need to find it backwards"""
            self.stat.getLastOccurrence(_data.getName()).setCategory(_action)
