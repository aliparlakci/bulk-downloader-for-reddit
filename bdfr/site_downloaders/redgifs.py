#!/usr/bin/env python3

import json
import re
from typing import Optional

from praw.models import Submission

from bdfr.exceptions import SiteDownloaderError
from bdfr.resource import Resource
from bdfr.site_authenticator import SiteAuthenticator
from bdfr.site_downloaders.base_downloader import BaseDownloader


class Redgifs(BaseDownloader):
    def __init__(self, post: Submission):
        super().__init__(post)

    def find_resources(self, authenticator: Optional[SiteAuthenticator] = None) -> list[Resource]:
        media_urls = self._get_link(self.post.url)
        return [Resource(self.post, m, Resource.retry_download(m), None) for m in media_urls]

    @staticmethod
    def _get_link(url: str) -> set[str]:
        try:
            redgif_id = re.match(r'.*/(.*?)/?$', url).group(1)
        except AttributeError:
            raise SiteDownloaderError(f'Could not extract Redgifs ID from {url}')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/90.0.4430.93 Safari/537.36',
        }

        content = Redgifs.retrieve_url(f'https://api.redgifs.com/v2/gifs/{redgif_id}', headers=headers)

        if content is None:
            raise SiteDownloaderError('Could not read the page source')

        try:
            response_json = json.loads(content.text)
        except json.JSONDecodeError as e:
            raise SiteDownloaderError(f'Received data was not valid JSON: {e}')

        out = set()
        try:
            if response_json['gif']['type'] == 1:  # type 1 is a video
                out.add(response_json['gif']['urls']['hd'])
            elif response_json['gif']['type'] == 2:  # type 2 is an image
                if response_json['gif']['gallery']:
                    content = Redgifs.retrieve_url(
                        f'https://api.redgifs.com/v2/gallery/{response_json["gif"]["gallery"]}',
                        headers=headers,
                    )
                    response_json = json.loads(content.text)
                    out = {p['urls']['hd'] for p in response_json['gifs']}
                else:
                    out.add(response_json['gif']['urls']['hd'])
            else:
                raise KeyError
        except (KeyError, AttributeError):
            raise SiteDownloaderError('Failed to find JSON data in page')

        return out
