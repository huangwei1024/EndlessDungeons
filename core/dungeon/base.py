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

class Room(object):
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	@property
	def left(self):
		return self.x

	@property
	def bottom(self):
		return self.y

	@property
	def right(self):
		return self.x + self.w - 1

	@property
	def top(self):
		return self.y + self.h - 1

	def expand(self, w, h):
		self.w += w
		self.h += h

	def move(self, x, y):
		self.x += x
		self.y += y

	def split(self, minx, miny, maxn=None):
		pass

	def __repr__(self):
		return 'Room 0x%x <x=%d, y=%d, w=%d, h=%d, x2=%d, y2=%d>' % (id(self), self.x, self.y, self.w, self.h, self.right, self.top) 

	def __str__(self):
		return 'Room <x=%d, y=%d, w=%d, h=%d, x2=%d, y2=%d>' % (self.x, self.y, self.w, self.h, self.right, self.top)

	def overlapping(self, r):
		return not ((self.right < r.x or r.right < self.x) and (self.top < r.y or r.top < self.y))
	

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