#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json


class FileNotFound(Exception):
    pass


class Test:

    def __init__(self):
        self.tests_db_ = self.__load_tests()

    def __load_tests(self):
        """Load test data from json file"""

        path = os.getcwd()
        json_file = "{0}/tests.json".format(path)

        try:
            with open(json_file, "r") as data_file:
                data = json.load(data_file)
        except Exception as error:
            raise FileNotFound("'tests.json' was not found")

        return data

    def get_tests_db(self):
        """Get List of all suite dict obj with labels and test cases"""
        return self.tests_db_

    def get_suite(self, suite_name):
        """Get suite dict obj with label name and test cases"""

        for suite in self.tests_db_:
            if suite['suite'] == suite_name:
                return suite

        return None

    def get_test_labels(self, suite_name):
        """takes suite name and returns a str list of test labels"""

        test_labels = []
        suite = self.get_suite(suite_name)
        test_cases = self.__get_test_cases(suite)
        for test in test_cases:
            test_labels.append(test['label'])

        return test_labels

    def get_module(self, test_label):
        """Get str list with script paths for a test label"""

        for suite in self.tests_db_:
            for test_case in self.__get_test_cases(suite):
                if test_label == test_case['label']:
                    return test_case['module']

    @staticmethod
    def __get_test_cases(suite):
        """takes a suite dict and returns test case dict list"""

        return suite['test_cases']
