#!/usr/bin/env python3

import json
import re
from typing import Optional

from cachetools import TTLCache, cached
from praw.models import Submission

from bdfr.exceptions import SiteDownloaderError
from bdfr.resource import Resource
from bdfr.site_authenticator import SiteAuthenticator
from bdfr.site_downloaders.redgifs import Redgifs


class Gfycat(Redgifs):
    def __init__(self, post: Submission):
        super().__init__(post)

    def find_resources(self, authenticator: Optional[SiteAuthenticator] = None) -> list[Resource]:
        return super().find_resources(authenticator)

    @staticmethod
    @cached(cache=TTLCache(maxsize=5, ttl=3420))
    def _get_auth_token() -> str:
        headers = {
            "content-type": "text/plain;charset=UTF-8",
            "host": "weblogin.gfycat.com",
            "origin": "https://gfycat.com",
        }
        payload = {"access_key": "Anr96uuqt9EdamSCwK4txKPjMsf2M95Rfa5FLLhPFucu8H5HTzeutyAa"}
        token = json.loads(
            Gfycat.post_url("https://weblogin.gfycat.com/oauth/webtoken", headers=headers, payload=payload).text
        )["access_token"]
        return token

    @staticmethod
    def _get_link(url: str) -> set[str]:
        gfycat_id = re.match(r".*/(.*?)(?:/?|-.*|\..{3-4})$", url).group(1)
        url = "https://gfycat.com/" + gfycat_id

        response = Gfycat.retrieve_url(url)
        if re.search(r"(redgifs|gifdeliverynetwork)", response.url):
            url = url.lower()
            return Redgifs._get_link(url)

        auth_token = Gfycat._get_auth_token()
        if not auth_token:
            raise SiteDownloaderError("Unable to retrieve Gfycat API token")

        headers = {
            "referer": "https://gfycat.com/",
            "origin": "https://gfycat.com",
            "content-type": "application/json",
            "Authorization": f"Bearer {auth_token}",
        }
        content = Gfycat.retrieve_url(f"https://api.gfycat.com/v1/gfycats/{gfycat_id}", headers=headers, initial=url)

        if content is None:
            raise SiteDownloaderError("Could not read the API source")

        try:
            response_json = json.loads(content.text)
        except json.JSONDecodeError as e:
            raise SiteDownloaderError(f"Received data was not valid JSON: {e}")

        try:
            out = response_json["gfyItem"]["mp4Url"]
        except (IndexError, KeyError, AttributeError) as e:
            raise SiteDownloaderError(f"Failed to download Gfycat link {url}: {e}")
        return {
            out,
        }
