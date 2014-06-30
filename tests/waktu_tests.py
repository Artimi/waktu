#!/usr/bin/env python2.7
#-*- coding: UTF-8 -*-

import unittest
import waktu
import tempfile
import os


class TestActivities(unittest.TestCase):

    def setUp(self):
        fd, self.file_path = tempfile.mkstemp()
        os.close(fd)
        self.activities = waktu.Activities(self.file_path)
        self.activity_list = [waktu.Activity('a1', 1),
                              waktu.Activity('a2', 2)]

    def tearDown(self):
        os.remove(self.file_path)

    def test_store_restore(self):
        self.activities.add(self.activity_list[0])
        self.activities.store()
        self.activities.add(self.activity_list[1])
        self.assertEqual(len(self.activities), 2)
        self.activities.restore()
        self.assertEqual(len(self.activities), 1)


class TestCategory(unittest.TestCase):

    def setUp(self):
        fd, self.file_path = tempfile.mkstemp()
        os.close(fd)
        self.categories = waktu.CategoryContainer(self.file_path)
        self.category_list = [waktu.Category('cat1', 'a1')]

    def tearDown(self):
        os.remove(self.file_path)

    def test_store_restore(self):
        self.categories.addCategory(self.category_list[0])
        self.categories.clearCategories()
        self.categories.restoreCategories()
        self.assertEqual(len(self.categories), 1)


class TestStats(unittest.TestCase):

    def setUp(self):
        fd, self.file_path = tempfile.mkstemp()
        os.close(fd)
        self.stats = waktu.Stats(self.file_path)
        self.activity_records = [waktu.ActivityRecord('cat1', waktu.Activity('a1', 1), 1, 2),
                                 waktu.ActivityRecord('cat2', waktu.Activity('a2', 2), 2, 3)]

    def tearDown(self):
        os.remove(self.file_path)

    def test_store_restore(self):
        self.stats.appendActivityRecord(self.activity_records[0])
        self.stats.storeRecords('19700101')
        self.stats.appendActivityRecord(self.activity_records[1])
        self.assertEqual(len(self.stats), 2)
        self.stats.updateRecords('19700101')
        self.assertEqual(len(self.stats), 1)
