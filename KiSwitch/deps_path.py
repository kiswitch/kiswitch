#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>

import os
import sys

DEPS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "deps")


class deps_path:
    def __init__(self, path=DEPS_PATH):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            while self.path in sys.path:
                sys.path.remove(self.path)
        except ValueError:
            pass
