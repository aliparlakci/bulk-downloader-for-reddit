#!/usr/bin/env python3
# coding=utf-8

import json
import logging

import dict2xml
import praw.models
import yaml

from bulkredditdownloader.archive_entry.submission_archive_entry import SubmissionArchiveEntry
from bulkredditdownloader.configuration import Configuration
from bulkredditdownloader.downloader import RedditDownloader
from bulkredditdownloader.exceptions import ArchiverError
from bulkredditdownloader.resource import Resource

logger = logging.getLogger(__name__)


class Archiver(RedditDownloader):
    def __init__(self, args: Configuration):
        super(Archiver, self).__init__(args)

    def download(self):
        for generator in self.reddit_lists:
            for submission in generator:
                logger.debug(f'Attempting to archive submission {submission.id}')
                self._write_submission(submission)

    def _write_submission(self, submission: praw.models.Submission):
        archive_entry = SubmissionArchiveEntry(submission)
        if self.args.format == 'json':
            self._write_submission_json(archive_entry)
        elif self.args.format == 'xml':
            self._write_submission_xml(archive_entry)
        elif self.args.format == 'yaml':
            self._write_submission_yaml(archive_entry)
        else:
            raise ArchiverError(f'Unknown format {self.args.format} given')
        logger.info(f'Record for submission {submission.id} written to disk')

    def _write_submission_json(self, entry: SubmissionArchiveEntry):
        resource = Resource(entry.source, '', '.json')
        content = json.dumps(entry.compile())
        self._write_content_to_disk(resource, content)

    def _write_submission_xml(self, entry: SubmissionArchiveEntry):
        resource = Resource(entry.source, '', '.xml')
        content = dict2xml.dict2xml(entry.compile(), wrap='root')
        self._write_content_to_disk(resource, content)

    def _write_submission_yaml(self, entry: SubmissionArchiveEntry):
        resource = Resource(entry.source, '', '.yaml')
        content = yaml.dump(entry.compile())
        self._write_content_to_disk(resource, content)

    def _write_content_to_disk(self, resource: Resource, content: str):
        file_path = self.file_name_formatter.format_path(resource, self.download_directory)
        file_path.parent.mkdir(exist_ok=True, parents=True)
        with open(file_path, 'w') as file:
            logger.debug(
                f'Writing submission {resource.source_submission.id} to file in {resource.extension[1:].upper()}'
                f' format at {file_path}')
            file.write(content)
