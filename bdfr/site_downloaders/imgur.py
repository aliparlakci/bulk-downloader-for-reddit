#!/usr/bin/env python3

import json
import re
from typing import Optional

from praw.models import Submission

from bdfr.exceptions import SiteDownloaderError
from bdfr.resource import Resource
from bdfr.site_authenticator import SiteAuthenticator
from bdfr.site_downloaders.base_downloader import BaseDownloader


class Imgur(BaseDownloader):
    def __init__(self, post: Submission):
        super().__init__(post)
        self.raw_data = {}

    def find_resources(self, authenticator: Optional[SiteAuthenticator] = None) -> list[Resource]:
        self.raw_data = self._get_data(self.post.url)

        out = []
        if "is_album" in self.raw_data:
            for image in self.raw_data["images"]:
                if "mp4" in image:
                    out.append(Resource(self.post, image["mp4"], Resource.retry_download(image["mp4"])))
                else:
                    out.append(Resource(self.post, image["link"], Resource.retry_download(image["link"])))
        else:
            if "mp4" in self.raw_data:
                out.append(Resource(self.post, self.raw_data["mp4"], Resource.retry_download(self.raw_data["mp4"])))
            else:
                out.append(Resource(self.post, self.raw_data["link"], Resource.retry_download(self.raw_data["link"])))
        return out

    @staticmethod
    def _get_data(link: str) -> dict:
        try:
            if link.endswith("/"):
                link = link.removesuffix("/")
            if re.search(r".*/(.*?)(gallery/|a/)", link):
                imgur_id = re.match(r".*/(?:gallery/|a/)(.*?)(?:/.*|\..{3,4})?$", link).group(1)
                api = f"https://api.imgur.com/3/album/{imgur_id}"
            else:
                imgur_id = re.match(r".*/(.*?)(?:_d)?(?:\..{0,})?$", link).group(1)
                api = f"https://api.imgur.com/3/image/{imgur_id}"
        except AttributeError:
            raise SiteDownloaderError(f"Could not extract Imgur ID from {link}")

        headers = {
            "referer": "https://imgur.com/",
            "origin": "https://imgur.com",
            "content-type": "application/json",
            "Authorization": "Client-ID 546c25a59c58ad7",
        }
        res = Imgur.retrieve_url(api, headers=headers, initial=link)

        try:
            image_dict = json.loads(res.text)
        except json.JSONDecodeError as e:
            raise SiteDownloaderError(f"Could not parse received response as JSON: {e}")

        return image_dict["data"]
