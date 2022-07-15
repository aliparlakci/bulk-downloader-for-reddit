#!/usr/bin/env python3
# coding=utf-8

from unittest.mock import MagicMock

import pytest

from bdfr.exceptions import NotADownloadableLinkError
from bdfr.resource import Resource
from bdfr.site_downloaders.youtube import Youtube


@pytest.mark.online
@pytest.mark.slow
@pytest.mark.parametrize(('test_url', 'expected_hash'), (
    ('https://www.youtube.com/watch?v=uSm2VDgRIUs', '2d60b54582df5b95ec72bb00b580d2ff'),
    ('https://www.youtube.com/watch?v=GcI7nxQj7HA', '5db0fc92a0a7fb9ac91e63505eea9cf0'),
    ('https://youtu.be/TMqPOlp4tNo', 'f68c00b018162857f3df4844c45302e7'),  # Age restricted
))
def test_find_resources_good(test_url: str, expected_hash: str):
    test_submission = MagicMock()
    test_submission.url = test_url
    downloader = Youtube(test_submission)
    resources = downloader.find_resources()
    assert len(resources) == 1
    assert isinstance(resources[0], Resource)
    resources[0].download()
    assert resources[0].hash.hexdigest() == expected_hash


@pytest.mark.online
@pytest.mark.parametrize('test_url', (
    'https://www.polygon.com/disney-plus/2020/5/14/21249881/gargoyles-animated-series-disney-plus-greg-weisman'
    '-interview-oj-simpson-goliath-chronicles',
))
def test_find_resources_bad(test_url: str):
    test_submission = MagicMock()
    test_submission.url = test_url
    downloader = Youtube(test_submission)
    with pytest.raises(NotADownloadableLinkError):
        downloader.find_resources()
