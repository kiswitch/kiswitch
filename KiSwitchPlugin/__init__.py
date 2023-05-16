#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>

try:
    from KiSwitchPlugin.plugin.plugin import KiSwitchPluginGenerator, KiSwitchPluginImporter

    print('Loading KiSwitch Plugins')

    KiSwitchPluginGenerator().register()
    # KiSwitchPluginImporter().register()

except Exception as e:
    from KiSwitchPlugin.util import logException
    logException(e, 'KiSwitchPlugin')
