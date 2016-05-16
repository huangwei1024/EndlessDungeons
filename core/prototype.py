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


class Prototype(object):
	@property
	def char(self):
		return self.Char

	def serialize(self):
		return self.char

	@staticmethod
	def deserialize(s):
		raise NotImplementedError('deserialize')

	def __getattr__(self, name):
		return None

class Objectype(Prototype):
	@property
	def objectization(self):
		return True
	
class Walkable(Prototype):
	@property
	def walkable(self):
		return True
	
class Visible(Prototype):
	@property
	def visible(self):
		return True
	
class Lockable(Prototype):
	def __init__(self, lock=True, check=None):
		self.__locked = lock
		self.__check = check

	@property
	def lockable(self):
		return True

	@property
	def locked(self):
		return self.__locked

	def unlock(self):
		if self.__locked:
			if self.__check and self.__check():
				self.__locked = False


class _VisibleObject(Objectype, Visible):
	pass