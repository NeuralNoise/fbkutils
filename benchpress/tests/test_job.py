#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

from collections import defaultdict
import unittest
from unittest.mock import MagicMock

from benchpress.lib.job import BenchmarkJob
from benchpress.lib.metrics import Metrics


class TestJob(unittest.TestCase):

    def test_validate_metrics(self):
        """Metrics with keys that don't match definition raise an error"""
        config = defaultdict(str)
        config['args'] = {}

        config['metrics'] = ['rps']
        job = BenchmarkJob(config, MagicMock())
        with self.assertRaises(AssertionError):
            job.validate_metrics(Metrics({}))
        with self.assertRaises(AssertionError):
            job.validate_metrics(Metrics({'latency': {'p50': 1}}))

        self.assertTrue(job.validate_metrics(Metrics({'rps': 1})))

        config['metrics'] = {'latency': ['p50', 'p95']}
        job = BenchmarkJob(config, MagicMock())
        self.assertTrue(job.validate_metrics(
            Metrics({'latency': {'p50': 1, 'p95': 2}})))

    def test_strip_metrics(self):
        """Metrics with keys that aren't in definition are removed"""
        config = defaultdict(str)
        config['args'] = {}

        config['metrics'] = ['rps']
        job = BenchmarkJob(config, MagicMock())

        # an empty set of metrics should stay empty
        stripped = job.strip_metrics(Metrics({}))
        self.assertEqual(len(stripped.metrics_list()), 0)

        # only passing the desired metric should stay the same
        stripped = job.strip_metrics(Metrics({'rps': 1}))
        self.assertEqual(len(stripped.metrics_list()), 1)

        # passing in more metrics should give just the requested ones
        stripped = job.strip_metrics(Metrics({'rps': 1, 'extra': 2}))
        self.assertEqual(len(stripped.metrics_list()), 1)

    def test_arg_list(self):
        """Argument list is formatted correctly with lists or dicts"""
        self.assertListEqual(
            ['--output-format=json', 'a'],
            BenchmarkJob.arg_list(['--output-format=json', 'a']))

        self.assertListEqual(
            ['--output-format', 'json', '--file'],
            BenchmarkJob.arg_list({'output-format': 'json', 'file': None}))


if __name__ == '__main__':
    unittest.main()
