#!/usr/bin/env python3
# coding=utf-8

from unittest.mock import MagicMock

import pytest

from bdfr.exceptions import NotADownloadableLinkError
from bdfr.resource import Resource
from bdfr.site_downloaders.vreddit import VReddit


@pytest.mark.online
@pytest.mark.slow
@pytest.mark.parametrize(('test_url', 'expected_hash'), (
    ('https://www.reddit.com/user/Xomb_Forever/comments/u5p2kj/hold_up/', '690cffe27a7884196437926c22897216'),
))
def test_find_resources_good(test_url: str, expected_hash: str):
    test_submission = MagicMock()
    test_submission.url = test_url
    downloader = VReddit(test_submission)
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
    downloader = VReddit(test_submission)
    with pytest.raises(NotADownloadableLinkError):
        downloader.find_resources()
