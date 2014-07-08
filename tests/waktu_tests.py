#!/usr/bin/env python2
#-*- coding: UTF-8 -*-

import unittest
from waktu.activity import Activity, Activities
from waktu.category import Category, CategoryContainer
from waktu.activityrecord import ActivityRecord
from waktu.stats import Stats
import tempfile
import os


class TestActivities(unittest.TestCase):

    def setUp(self):
        fd, self.file_path = tempfile.mkstemp()
        os.close(fd)
        self.activities = Activities(self.file_path)
        self.activity_list = [Activity('a1', name='name1'),
                              Activity('a2', name='name2')]

    def tearDown(self):
        os.remove(self.file_path)

    def test_store_restore(self):
        self.activities.add(self.activity_list[0])
        self.activities.store()
        self.activities.add(self.activity_list[1])
        self.assertEqual(len(self.activities), 2)
        self.activities.restore()
        self.assertEqual(len(self.activities), 1)

    def test_iter(self):
        self.activities.add(self.activity_list[0])
        self.activities.add(self.activity_list[1])
        for pair in zip(self.activities, self.activity_list):
            self.assertEqual(pair[0], pair[1])


class TestCategory(unittest.TestCase):

    def setUp(self):
        fd, self.file_path = tempfile.mkstemp()
        os.close(fd)
        self.categories = CategoryContainer(self.file_path)
        self.category_list = [Category('cat1', 'a1')]

    def tearDown(self):
        os.remove(self.file_path)

    def test_store_restore(self):
        self.categories.add(self.category_list[0])
        self.categories.clear()
        self.categories.restore()
        self.assertEqual(len(self.categories), 1)


class TestStats(unittest.TestCase):

    def setUp(self):
        fd, self.file_path = tempfile.mkstemp()
        os.close(fd)
        self.stats = Stats(self.file_path)
        self.activity_records = [ActivityRecord('cat1', Activity('a1', 1), 1, 2),
                                 ActivityRecord('cat2', Activity('a2', 2), 2, 3)]

    def tearDown(self):
        os.remove(self.file_path)

    def test_store_restore(self):
        self.stats.append(self.activity_records[0])
        self.stats.store('19700101')
        self.stats.append(self.activity_records[1])
        self.assertEqual(len(self.stats), 2)
        self.stats.restore('19700101')
        self.assertEqual(len(self.stats), 1)
