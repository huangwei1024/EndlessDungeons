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

class Door(_VisibleObject, Walkable, Lockable):
	Char = '+'

	@property
	def char(self):
		return Door.Char if self.locked else Road.Char

class Upstair(_VisibleObject, Walkable):
	Char = 'S'

class Downstair(_VisibleObject, Walkable):
	Char = 'T'




