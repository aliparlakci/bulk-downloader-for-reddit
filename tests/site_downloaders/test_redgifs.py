#!/usr/bin/env python3
# coding=utf-8

from unittest.mock import Mock

import pytest

from bdfr.resource import Resource
from bdfr.site_downloaders.redgifs import Redgifs


@pytest.mark.online
@pytest.mark.parametrize(('test_url', 'expected'), (
    ('https://redgifs.com/watch/frighteningvictorioussalamander',
     {'https://thumbs2.redgifs.com/FrighteningVictoriousSalamander.mp4'}),
    ('https://redgifs.com/watch/springgreendecisivetaruca',
     {'https://thumbs2.redgifs.com/SpringgreenDecisiveTaruca.mp4'}),
    ('https://www.redgifs.com/watch/palegoldenrodrawhalibut',
     {'https://thumbs2.redgifs.com/PalegoldenrodRawHalibut.mp4'}),
    ('https://redgifs.com/watch/hollowintentsnowyowl',
     {'https://thumbs2.redgifs.com/HollowIntentSnowyowl-large.jpg'}),
    ('https://www.redgifs.com/watch/lustrousstickywaxwing',
     {'https://thumbs2.redgifs.com/EntireEnchantingHypsilophodon-large.jpg',
      'https://thumbs2.redgifs.com/FancyMagnificentAdamsstaghornedbeetle-large.jpg',
      'https://thumbs2.redgifs.com/LustrousStickyWaxwing-large.jpg',
      'https://thumbs2.redgifs.com/ParchedWindyArmyworm-large.jpg',
      'https://thumbs2.redgifs.com/ThunderousColorlessErmine-large.jpg',
      'https://thumbs2.redgifs.com/UnripeUnkemptWoodpecker-large.jpg'}),
))
def test_get_link(test_url: str, expected: set[str]):
    result = Redgifs._get_link(test_url)
    assert result == expected


@pytest.mark.online
@pytest.mark.parametrize(('test_url', 'expected_hashes'), (
    ('https://redgifs.com/watch/frighteningvictorioussalamander', {'4007c35d9e1f4b67091b5f12cffda00a'}),
    ('https://redgifs.com/watch/springgreendecisivetaruca', {'8dac487ac49a1f18cc1b4dabe23f0869'}),
    ('https://redgifs.com/watch/leafysaltydungbeetle', {'076792c660b9c024c0471ef4759af8bd'}),
    ('https://www.redgifs.com/watch/palegoldenrodrawhalibut', {'46d5aa77fe80c6407de1ecc92801c10e'}),
    ('https://redgifs.com/watch/hollowintentsnowyowl',
     {'5ee51fa15e0a58e98f11dea6a6cca771'}),
    ('https://www.redgifs.com/watch/lustrousstickywaxwing',
     {'b461e55664f07bed8d2f41d8586728fa',
      '30ba079a8ed7d7adf17929dc3064c10f',
      '0d4f149d170d29fc2f015c1121bab18b',
      '53987d99cfd77fd65b5fdade3718f9f1',
      'fb2e7d972846b83bf4016447d3060d60',
      '44fb28f72ec9a5cca63fa4369ab4f672'}),
))
def test_download_resource(test_url: str, expected_hashes: set[str]):
    mock_submission = Mock()
    mock_submission.url = test_url
    test_site = Redgifs(mock_submission)
    results = test_site.find_resources()
    assert all([isinstance(res, Resource) for res in results])
    [res.download() for res in results]
    hashes = set([res.hash.hexdigest() for res in results])
    assert hashes == set(expected_hashes)
