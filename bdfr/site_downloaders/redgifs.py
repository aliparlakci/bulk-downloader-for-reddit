#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import os
import tempfile
from typing import Optional

import requests
from praw.models import Submission

from bdfr.exceptions import SiteDownloaderError
from bdfr.resource import Resource
from bdfr.site_authenticator import SiteAuthenticator
from bdfr.site_downloaders.base_downloader import BaseDownloader


class Redgifs(BaseDownloader):
    # Setting temp token path. Probably would be better somewhere else, but os temp works.
    TOKEN_FILE_PATH = os.path.join(tempfile.gettempdir(), "redgifs_token.txt")

    def __init__(self, post: Submission):
        super().__init__(post)

    def find_resources(self, authenticator: Optional[SiteAuthenticator] = None) -> list[Resource]:
        media_urls = self._get_link(self.post.url)
        return [Resource(self.post, m, Resource.retry_download(m), None) for m in media_urls]

    ### Temporary auth token handling ###
    def _load_token(self, url) -> Optional[str]:
        try:
            with open(self.TOKEN_FILE_PATH, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            print("\n-=-=-=-=-=-=-=-=-=-=-=-\nRedgifs API token file not found, retrieving new token")
            self._get_token(self, url)
            with open(self.TOKEN_FILE_PATH, "r") as file:
                return file.read().strip()

    def _save_token(self, token: str, url):
        print(f"Writing Redgifs temporary API token to {self.TOKEN_FILE_PATH}")
        with open(self.TOKEN_FILE_PATH, "w") as file:
            file.write(token)
        print(f"Success!\n\nNew temporary token is: {token}\n-=-=-=-=-=-=-=-=-=-=-=-\n")
        return token

    def _get_token(self, redgif_id, other=None) -> str:
        try:
            print("Attempting to retrieve new temporary Redgifs API token")
            response = self.retrieve_url("https://api.redgifs.com/v2/auth/temporary")
            auth_token = json.loads(response.text)["token"]

            self._save_token(self, auth_token, redgif_id)
        except Exception as e:
            raise SiteDownloaderError(f"Failed to retrieve Redgifs API token: {e}")
        return auth_token
    ### End temporary auth token handling ###

    @staticmethod
    def _get_id(url: str) -> str:
        try:
            if url.endswith("/"):
                url = url.removesuffix("/")
            redgif_id = re.match(r".*/(.*?)(?:#.*|\?.*|\..{0,})?$", url).group(1).lower()
            if redgif_id.endswith("-mobile"):
                redgif_id = redgif_id.removesuffix("-mobile")
        except AttributeError:
            raise SiteDownloaderError(f"Could not extract Redgifs ID from {url}")
        return redgif_id

    @staticmethod
    def _get_link(url: str) -> set[str]:
        redgif_id = Redgifs._get_id(url)

        # Passing url here. Probably don't need to.
        auth_token = Redgifs._load_token(Redgifs, url)

        headers = {
            "referer": "https://www.redgifs.com/",
            "origin": "https://www.redgifs.com",
            "content-type": "application/json",
            "Authorization": f"Bearer {auth_token}",
        }

        content = Redgifs.retrieve_url(f"https://api.redgifs.com/v2/gifs/{redgif_id}", headers=headers)

        if content is None:
            raise SiteDownloaderError("Could not read the page source")

        try:
            response_json = json.loads(content.text)
        except json.JSONDecodeError as e:
            raise SiteDownloaderError(f"Received data was not valid JSON: {e}")

        out = set()
        try:
            if response_json["gif"]["type"] == 1:  # type 1 is a video
                if requests.get(response_json["gif"]["urls"]["hd"], headers=headers).ok:
                    out.add(response_json["gif"]["urls"]["hd"])
                else:
                    out.add(response_json["gif"]["urls"]["sd"])
            elif response_json["gif"]["type"] == 2:  # type 2 is an image
                if response_json["gif"]["gallery"]:
                    content = Redgifs.retrieve_url(
                        f'https://api.redgifs.com/v2/gallery/{response_json["gif"]["gallery"]}'
                    )
                    response_json = json.loads(content.text)
                    out = {p["urls"]["hd"] for p in response_json["gifs"]}
                else:
                    out.add(response_json["gif"]["urls"]["hd"])
            else:
                raise KeyError
        except (KeyError, AttributeError):
            raise SiteDownloaderError("Failed to find JSON data in page")

        # Update subdomain if old one is returned
        out = {re.sub("thumbs2", "thumbs3", link) for link in out}
        out = {re.sub("thumbs3", "thumbs4", link) for link in out}
        return out
