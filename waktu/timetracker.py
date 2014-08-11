#-*- coding: UTF-8 -*-
"""
Waktu module of timetracker core. This is functional core of Waktu. This module (and objects inside) are designed to track application in background and report results back.
"""
from gi.repository import Wnck, Gdk, GObject, Notify, GLib
from activityrecord import ActivityRecord
from threading import Thread, Event
from time import sleep, time
import copy
import logging


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
        self.last_activity = ActivityRecord()
        self.screen = Wnck.Screen.get_default()
        self.n = Notify.Notification()

        if configuration['state']:
            self.track.set()
        else:
            self.track.clear()

        if configuration['mode']:
            self.mode.set()
        else:
            self.mode.clear()

    def run(self):
        """Start tracking user activities"""

        while not self.stopthread.isSet():
            sleep(1)

            # Skip tracking if it's disabled
            if not self.track.isSet():
                continue

            Gdk.threads_enter()
            GObject.idle_add(self.screen.force_update)
            active_window = self.screen.get_active_window()

            # Skip if there is no active window
            if active_window is None:
                Gdk.threads_leave()
                continue

            app_name = active_window.get_application().get_name()
            app_pid = active_window.get_application().get_pid()

            # If the learning mode is activive, only append an activity
            if self.mode.isSet():
                self.activities.add(app_name)
                Gdk.threads_leave()
                continue

            if self.last_activity.activity.pid == app_pid:
                # Still the same activity, just actualize the end time
                self.last_activity.end_time = time()

            else:
                # New activity, actualize the lastActivity and append the new activity
                if self.last_activity.activity.pid != 0:
                    tmp = copy.deepcopy(self.last_activity)
                    self.stat.append(tmp)
                    self.activities.add(tmp.activity.name)
                    logging.debug("DBG: Zmena aktivity! Ulozena aktivita %s (%s)" % (tmp.activity.name, tmp.category))

                self.last_activity.activity.name = app_name
                self.last_activity.activity.pid = app_pid
                self.last_activity.category = 'OTHER'
                self.set_correct_category()
                self.last_activity.start_time = time()
                self.last_activity.end_time = time()

            Gdk.threads_leave()

        if self.track.isSet() and not self.mode.isSet():
            tmp = copy.deepcopy(self.last_activity)
            self.stat.append(tmp)
            logging.debug("DBG: Ulozena aktivita %s (%s)" % (tmp.activity.name, tmp.category))

        # Store all records to file to make them persistent
        self.stat.store()
        self.activities.store()

    def stop(self):
        """Stop the tracking system, uses id stored in initialization"""
        self.stopthread.set()

    def set_correct_category(self, activity=None):
        """Find out category where the activity belongs to"""
        if activity is None:
            activity = self.last_activity.activity

        activity_categories = self.categories.get_containing_categories(activity)
        if len(activity_categories) == 0:
            # The activity isn't in any category
            self.last_activity.category = 'OTHER'
        elif len(activity_categories) == 1:
            # The activity is in exactly one category
            self.last_activity.category = activity_categories[0].name
        else:
            # The activity is in more than one category. The Waktu needs to ask user.
            last_occurrence = self.stat.get_last_occurrence(activity.name)
            # 10 minutes is the default time to remember users choice
            if last_occurrence is None or (time() - last_occurrence.endTime) > 600:
                self.ask_user(activity, activity_categories)
            else:
                self.last_activity.category = last_occurrence.category

    def ask_user(self, activity, categories):
        """Creates a notification and asks a user where the activity belongs to"""
        if not Notify.is_initted():
            Notify.init('Waktu')

        self.n.clear_hints()
        self.n.clear_actions()
        self.n.set_property('summary', 'Kam patří aktivita %s?' % activity.name)
        self.n.set_property('body', 'Zdá se, že tuto aktivitu máte zvolenou ve více kategoriích. Zvolte, prosím, níže'
                                    ' jednu, do které spadá tato aktivita práve teď.')
        self.n.set_property('icon_name', 'dialog-question')
        self.n.set_urgency(Notify.Urgency.NORMAL)
        self.n.set_timeout(Notify.EXPIRES_NEVER)
        self.n.set_hint("resident", GLib.Variant('b', True))

        for cat in categories:
            self.n.add_action(cat.name, cat.name, self.get_user_answer, activity, None)

        self.n.add_action("OTHER", "Jinam", self.get_user_answer, activity, None)

        self.n.show()

    def get_user_answer(self, n, action, data):
        """Process user answer and delegate result"""
        n.close()

        if self.last_activity.activity.name == data.name:
            # The focused app is still the same
            self.last_activity.category = action
        else:
            # There is another activity, need to find it backwards
            self.stat.get_last_occurrence(data.name).category = action
