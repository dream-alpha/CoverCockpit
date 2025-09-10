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


from Components.config import config, ConfigSubsection, ConfigSet, ConfigSelection
from .Debug import log_levels, logger, initLogging


class ConfigInit():
    def __init__(self):
        logger.info("...")
        config.plugins.covercockpit = ConfigSubsection()
        config.plugins.covercockpit.search_prio = ConfigSet([], [])
        if not config.plugins.covercockpit.search_prio.value:
            config.plugins.covercockpit.search_prio.value = [
                "tvfa_id", "tvh_id", "tvs_id"]
            config.plugins.covercockpit.search_prio.save()
        config.plugins.covercockpit.debug_log_level = ConfigSelection(
            default="INFO", choices=list(log_levels.keys()))
        initLogging()
