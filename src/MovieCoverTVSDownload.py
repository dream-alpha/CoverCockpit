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


import json
from datetime import datetime, timedelta
from .Debug import logger
from .MovieCoverUNIDownload import MovieCoverUNIDownload
from .WebRequests import WebRequests


class MovieCoverTVSDownload(WebRequests, MovieCoverUNIDownload):

	def __init__(self):
		WebRequests.__init__(self)
		MovieCoverUNIDownload.__init__(self)

	def getCoverContent(self, channel_id, _event_start):
		logger.debug("channel_id: %s", channel_id)
		content = []
		for x in range(-1, 2):
			day = (datetime.now() + timedelta(days=x)).strftime("%Y-%m-%d")
			content_url = "https://live.tvspielfilm.de/static/broadcast/list/%s/%s" % (channel_id, day)
			logger.debug("content_url: %s", content_url)
			r_content = self.getContent(content_url)
			if r_content and "Error" not in r_content:
				content.extend(json.loads(r_content))
		return content

	def parseEvents(self, _channel_id, content, event_start, length):
		logger.info("...")
		cover_url = ""
		cover_title = ""
		for event in content:
			# logger.debug("event: %s", str(event))
			url = ""
			title = event.get("title", "n/a")
			timestart = event.get("timestart", 0)
			if "images" in event:
				url = event["images"][0]["size4"]

			if not self.findEvent(timestart, event_start, length):
				logger.debug(">>> saving: url: %s, title: %s", url, title)
				cover_title = title
				cover_url = url
			else:
				logger.debug(">>> found: url: %s, title: %s", cover_url, cover_title)
				return cover_url
		logger.debug(">>> not found: url: %s, title: %s", cover_url, cover_title)
		return cover_url
