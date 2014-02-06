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
