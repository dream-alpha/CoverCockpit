#!/usr/bin/python
# coding=utf-8
#
# Copyright (C) 2018-2025 by dream-alpha
#
# In case of reuse of this source code please do not remove this copyright.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For more information on the GNU General Public License see:
# <http://www.gnu.org/licenses/>.


from datetime import datetime
from .Debug import logger
from .MovieCoverUNIDownload import MovieCoverUNIDownload
from .WebRequests import WebRequests
from .TVSUtils import tvs_parse, tvs_parse_details


class MovieCoverTVSDownload(WebRequests, MovieCoverUNIDownload):

    def __init__(self):
        WebRequests.__init__(self)
        MovieCoverUNIDownload.__init__(self)

    def getCoverContent(self, channel_id, _event_start):
        logger.debug("channel_id: %s", channel_id)
        events = []
        day = datetime.now().strftime("%Y-%m-%d")
        for page in [1, 2]:
            content_url = 'https://www.tvspielfilm.de/tv-programm/sendungen/?channel=%s&date=%s&page=%s' % (
                channel_id, day, page)
            logger.debug("content_url: %s", content_url)
            r_content = self.getContent(content_url)
            if r_content and "Error" not in r_content:
                events += tvs_parse(r_content)
        return events

    def getUrl(self, event):
        photo_url = ""
        url = event.get("urlsendung", "")
        if url:
            content = self.getContent(url)
            event = tvs_parse_details(content, {})
            photo_url = event.get("photo_url", "")
        return photo_url

    def parseEvents(self, _channel_id, events, event_start, length):
        logger.info("...")
        cover_url = ""
        cover_title = ""
        for event in events:
            logger.debug("event: %s", str(event))
            url = ""
            title = event.get("title", "n/a")
            timestart = event.get("startTime", 0)
            current_event = dict(event)

            if not self.findEvent(timestart, event_start, length):
                logger.debug(">>> saving: url: %s, title: %s", url, title)
                cover_title = title
                cover_url = self.getUrl(current_event)
            else:
                logger.debug(">>> found: url: %s, title: %s",
                             cover_url, cover_title)
                return cover_url
        logger.debug(">>> not found: url: %s, title: %s",
                     cover_url, cover_title)
        return cover_url
