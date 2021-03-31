#!/usr/bin/env python3
# coding=utf-8

import logging

import praw.models

from bulkredditdownloader.archive_entry.base_archive_entry import BaseArchiveEntry

logger = logging.getLogger(__name__)


class SubmissionArchiveEntry(BaseArchiveEntry):
    def __init__(self, submission: praw.models.Submission):
        super(SubmissionArchiveEntry, self).__init__(submission)
        self.comments: list[dict] = []

    def compile(self) -> dict:
        self._fill_entry()
        out = self.post_details
        out['comments'] = self.comments
        return out

    def _fill_entry(self):
        self._get_comments()
        self._get_post_details()

    def _get_post_details(self):
        self.post_details = {
            'title': self.source.title,
            'name': self.source.name,
            'url': self.source.url,
            'selftext': self.source.selftext,
            'score': self.source.score,
            'upvote_ratio': self.source.upvote_ratio,
            'permalink': self.source.permalink,
            'id': self.source.id,
            'author': self.source.author.name if self.source.author else 'DELETED',
            'link_flair_text': self.source.link_flair_text,
            'num_comments': self.source.num_comments,
            'over_18': self.source.over_18,
            'created_utc': self.source.created_utc,
        }

    def _get_comments(self):
        logger.debug(f'Retrieving full comment tree for submission {self.source.id}')
        self.source.comments.replace_more(0)
        for top_level_comment in self.source.comments:
            self.comments.append(self._convert_comment_to_dict(top_level_comment))
