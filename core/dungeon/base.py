#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 HuangWei (http://huangwei.pro)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import inspect
from collections import namedtuple

Room = namedtuple('Room', ('x', 'y', 'w', 'h'))

def isRoomOverlapping(r1, r2):
	return not ((r1.x + r1.w < r2.x or r2.x + r2.w < r1.x) and (r1.y + r1.h < r2.y or r2.y + r2.h < r1.y))


class GeneratorBase(object):
	def __init__(self):
		args = inspect.getargspec(self.__init__)
		self.__args = {k: None for k in args.args}
		if args.defaults:
			self.__args = {k: args.defaults[i] for i, k in enumerate(args.args[len(args.args) - len(args.defaults):])}
		self.__args.pop('w', None)
		self.__args.pop('h', None)
		self.__args.pop('width', None)
		self.__args.pop('height', None)

	def generate(self):
		raise NotImplementedError('generate')

	def getRooms(self):
		raise NotImplementedError('getRooms')

	def getSettings(self):
		return self.__args