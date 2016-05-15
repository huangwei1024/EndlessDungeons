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

import msgpack

from block import (
	Space
)

class Grid(object):
	def __init__(self, block, obj=None):
		self.block = block
		self.obj = obj

	def serialize(self):
		return self.block.char

	@staticmethod
	def deserialize(s):
		pass

class GridsMatrix(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.mat = [[Grid(Space()) for x in xrange(width)] for y in xrange(height)]

	def serialize(self):
		return msgpack.packb([[self.mat[y][x].serialize() for x in xrange(width)] for y in xrange(height)])

	@staticmethod
	def deserialize(s):
		mat = msgpack.unpackb(s)
		height = len(mat)
		width = len(mat[0])
		mat = [[Grid.deserialize(mat[y][x]) for x in xrange(width)] for y in xrange(height)]
		ret = GridsMatrix(width, height)
		ret.mat = mat
		return ret
















