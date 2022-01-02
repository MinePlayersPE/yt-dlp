# coding: utf-8
from .common import InfoExtractor

from ..utils import (
    int_or_none,
    str_or_none,
    urljoin,
)

class MusicDexBaseIE(InfoExtractor):
    def _parse_track(self, track):
        return {
            'id': str(track['id']),
            'title': track['name'],
            'description': track.get('description'),
            'duration': int_or_none(track.get('duration'), scale=1000),
            'artist': ', '.join(traverse_obj(
                track, ('artists', ..., 'name'), expected_type=str_or_none, default=[])) or None,
            'genre': ', '.join(traverse_obj(
                track, ('genres', ..., 'name'), expected_type=str_or_none, default=[])) or None,
            'url': urljoin(
                'https://www.musicdex.org/', track['url']),
            'like_count': int_or_none(track.get('likes_count')),
            'view_count': int_or_none(track.get('plays')),
            'repost_count': int_or_none(track.get('reposts_count')),
            'comment_count': int_or_none(track.get('comments_count')),

        }

class MusicDexIE(MusicDexBaseIE):
    _VALID_URL = r'https?://(?:www\.)?musicdex\.org/track/(?P<id>[0-9]+)'
    _TESTS = [{
        'url': 'https://www.musicdex.org/track/306/dual-existence',
        'md5': 'TODO: md5 sum of the first 10241 bytes of the video file (use --test)',
        'info_dict': {
            'id': '42',
            'ext': 'mp4',
            'title': 'Video title goes here',
            'thumbnail': r're:^https?://.*\.jpg$',
            # TODO more properties, either as:
            # * A value
            # * MD5 checksum; start the string with md5:
            # * A regular expression; start the string with re:
            # * Any Python type (for example int or float)
        }
    }]

    def _real_extract(self, url):
        track_id = self._match_id(url)

        return self._parse_track(self._download_json(
            f'https://www.musicdex.org/secure/tracks/{track_id}?defaultRelations=true&forEditing=true', track_id)['track'])
