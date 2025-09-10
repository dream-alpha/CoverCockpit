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


import os
from twisted.internet import threads, reactor
from Components.config import config
from .Debug import logger
from .MovieCoverTVFADownload import MovieCoverTVFADownload
from .MovieCoverTVHDownload import MovieCoverTVHDownload
from .MovieCoverTVSDownload import MovieCoverTVSDownload
from .WebRequests import WebRequests


class CoverCockpit(WebRequests):

    def __init__(self):
        WebRequests.__init__(self)
        self.cover_source_ids = config.plugins.covercockpit.search_prio.value  # priority
        logger.debug("cover_source_ids: %s", self.cover_source_ids)
        self.cover_sources = {
            "tvfa_id": MovieCoverTVFADownload,
            "tvh_id": MovieCoverTVHDownload,
            "tvs_id": MovieCoverTVSDownload
        }

    def downloadCover(self, path, service_ref, event_start, length, callback):
        logger.info("...")
        logger.debug("cover_source_ids: %s", self.cover_source_ids)
        for cover_source_id in self.cover_source_ids:
            logger.debug("cover_source_id: %s", cover_source_id)
            cover_url = self.cover_sources[cover_source_id]().getSourceMovieCover(
                path, cover_source_id, service_ref, event_start, length)
            if cover_url:
                if self.downloadFile(cover_url, os.path.splitext(path)[0] + ".jpg"):
                    break
        reactor.callFromThread(callback, path)

    def getMovieCover(self, path, service_ref, event_start=0, length=0, cover_source_id="", callback=None):
        logger.info("path: %s, cover_source_id: %s", path, cover_source_id)
        if not cover_source_id or cover_source_id not in self.cover_source_ids:
            cover_source_id = "auto"
        if cover_source_id != "auto":
            self.cover_source_ids = [cover_source_id]
        threads.deferToThread(self.downloadCover, path,
                              service_ref, event_start, length, callback)
