#!/usr/bin/env python3
# coding=utf-8

import praw
import pytest

from bulkredditdownloader.archive_entry.comment_archive_entry import CommentArchiveEntry


@pytest.mark.online
@pytest.mark.reddit
@pytest.mark.parametrize(('test_comment_id', 'expected_dict'), (
    ('gstd4hk', {
        'author': 'james_pic',
        'subreddit': 'Python',
        'submission': 'mgi4op',
    }),
))
def test_get_comment_details(test_comment_id: str, expected_dict: dict, reddit_instance: praw.Reddit):
    comment = reddit_instance.comment(id=test_comment_id)
    test_entry = CommentArchiveEntry(comment)
    result = test_entry.compile()
    assert all([result.get(key) == expected_dict[key] for key in expected_dict.keys()])
