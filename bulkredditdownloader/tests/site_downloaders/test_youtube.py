#!/usr/bin/env python3
# coding=utf-8

import praw
import pytest

from bulkredditdownloader.resource import Resource
from bulkredditdownloader.site_downloaders.youtube import Youtube


@pytest.mark.online
@pytest.mark.reddit
@pytest.mark.slow
@pytest.mark.parametrize(('test_submission_id', 'expected_hash'), (
    ('ltnoqp', '468136300a106c67f1463a7011a6db4a'),
    ('m2l5oo', 'a70512f7782f13922258297bb12055d9'),
))
def test_find_resources(test_submission_id: str, expected_hash: str, reddit_instance: praw.Reddit):
    test_submission = reddit_instance.submission(id=test_submission_id)
    downloader = Youtube(test_submission)
    resources = downloader.find_resources()
    assert len(resources) == 1
    assert isinstance(resources[0], Resource)
    resources[0].download()
    assert resources[0].hash.hexdigest() == expected_hash
