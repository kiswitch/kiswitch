#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Rafael Silva <perigoso@riseup.net>

import os

PLUGINPATH = os.path.dirname(os.path.realpath(__file__))

def logException(e: Exception, log_name: str) -> None:
	import traceback
	from datetime import datetime

	trace = traceback.format_exc()
	print(trace)

	log_file = os.path.join(PLUGINPATH, f'{log_name}.log')
	with open(log_file, 'a') as f:
		f.write(f'\n{datetime.now()}:\n{trace}')
