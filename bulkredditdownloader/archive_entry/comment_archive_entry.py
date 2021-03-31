#!/usr/bin/env python3
# coding=utf-8

import logging

import praw.models

from bulkredditdownloader.archive_entry.base_archive_entry import BaseArchiveEntry

logger = logging.getLogger(__name__)


class CommentArchiveEntry(BaseArchiveEntry):
    def __init__(self, comment: praw.models.Comment):
        super(CommentArchiveEntry, self).__init__(comment)

    def compile(self) -> dict:
        self.post_details = self._convert_comment_to_dict(self.source)
        return self.post_details
