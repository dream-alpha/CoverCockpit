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


from Plugins.Plugin import PluginDescriptor
from .Debug import logger
from .Version import VERSION
from .PluginUtils import WHERE_COVER_DOWNLOAD
from .CoverCockpit import CoverCockpit
from .ConfigInit import ConfigInit


def downloadCover(path, service_ref, event_start=0, length=0, cover_source_id="", callback=None, **__kwargs):
    CoverCockpit().getMovieCover(path, service_ref,
                                 event_start, length, cover_source_id, callback)


def autoStart(reason, **kwargs):
    if reason == 0:  # startup
        if "session" in kwargs:
            logger.info("+++ Version: %s starts...", VERSION)
    elif reason == 1:  # shutdown
        logger.info("--- shutdown")


def Plugins(**__kwargs):
    ConfigInit()
    return [
        PluginDescriptor(
            where=[
                PluginDescriptor.WHERE_AUTOSTART,
                PluginDescriptor.WHERE_SESSIONSTART
            ],
            fnc=autoStart
        ),
        PluginDescriptor(
            name="CoverCockpit",
            description="Cover Downloads",
            where=WHERE_COVER_DOWNLOAD,
            fnc=downloadCover
        ),
    ]
