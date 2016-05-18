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

from prototype import (
	Prototype,
	Objectype,
	Walkable,
	Visible,
	Lockable,

	_VisibleObject
)

class Space(Prototype):
	Char = ' '

class Wall(_VisibleObject):
	Char = '#'

class Road(_VisibleObject, Walkable):
	Char = '.'
	IDChars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

	def __init__(self, id=None):
		self.id = id

	@property
	def char(self):
		return self.IDChars[self.id] if self.id is not None else self.Char

class Door(_VisibleObject, Walkable, Lockable):
	LockedChar = '+'
	UnlockedChar = '-'

	@property
	def char(self):
		return Door.LockedChar if self.locked else Door.UnlockedChar

class Upstair(_VisibleObject, Walkable):
	Char = 'S'

class Downstair(_VisibleObject, Walkable):
	Char = 'T'




