#!/usr/bin/env python3
# coding=utf-8

import praw
import pytest

from bulkredditdownloader.exceptions import NotADownloadableLinkError
from bulkredditdownloader.site_downloaders.base_downloader import BaseDownloader
from bulkredditdownloader.site_downloaders.direct import Direct
from bulkredditdownloader.site_downloaders.download_factory import DownloadFactory
from bulkredditdownloader.site_downloaders.erome import Erome
from bulkredditdownloader.site_downloaders.gallery import Gallery
from bulkredditdownloader.site_downloaders.gfycat import Gfycat
from bulkredditdownloader.site_downloaders.gif_delivery_network import GifDeliveryNetwork
from bulkredditdownloader.site_downloaders.imgur import Imgur
from bulkredditdownloader.site_downloaders.redgifs import Redgifs
from bulkredditdownloader.site_downloaders.self_post import SelfPost
from bulkredditdownloader.site_downloaders.vreddit import VReddit
from bulkredditdownloader.site_downloaders.youtube import Youtube


@pytest.mark.online
@pytest.mark.reddit
@pytest.mark.parametrize(('test_submission_id', 'expected_class'), (
    ('lu8l8g', VReddit),
    ('lu29zn', SelfPost),
    ('lu2ykk', Direct),  # Imgur direct link
    ('luh2pd', Direct),  # Reddit direct link
    ('luo9eo', Imgur),  # Imgur .gifv link
    ('lumulo', Direct),  # Imgur direct link gif
    ('lui5t3', Imgur),
    ('lu93m7', Gallery),
    ('luf1nu', Gfycat),
    ('luxmgx', Erome),
    ('lupb4r', Youtube),
    ('lul6l7', Redgifs),
    ('luu376', GifDeliveryNetwork),
    ('m2l5oo', Youtube),
))
def test_factory_lever_good(test_submission_id: str, expected_class: BaseDownloader, reddit_instance: praw.Reddit):
    submission = reddit_instance.submission(id=test_submission_id)
    result = DownloadFactory.pull_lever(submission.url)
    assert result is expected_class


@pytest.mark.parametrize('test_url', (
    'random.com',
    'bad',
    'https://www.google.com/',
    'https://www.google.com',
    'https://www.google.com/test',
    'https://www.google.com/test/',
))
def test_factory_lever_bad(test_url: str):
    with pytest.raises(NotADownloadableLinkError):
        DownloadFactory.pull_lever(test_url)
