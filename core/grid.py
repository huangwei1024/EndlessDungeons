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

from block import Space, Wall

Directions8 = (
	(0, 1),
	(1, 0),
	(0, -1),
	(-1, 0),
	(1, 1),
	(-1, 1),
	(1, -1),
	(-1, -1),
)

class Grid(object):
	def __init__(self, block, obj=None):
		self.block = block
		self.obj = obj

	def serialize(self):
		return self.block.serialize()

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

	def set(self, x, y, block, obj=None):
		try:
			self.mat[y][x] = Grid(block, obj)
		except:
			print x, y, self.width, self.height
			raise

	def wrapWall(self):
		wallset = set()
		for y in xrange(self.height):
			for x in xrange(self.width):
				if not self.mat[y][x].block.visible:
					continue
				for d in Directions8:
					dx = x + d[0]
					dy = y + d[1]
					if dx < 0 or dy < 0 or dx >= self.width or dy >= self.height:
						continue
					if not self.mat[dy][dx].block.visible:
						wallset.add((dx, dy))
		for xy in wallset:
			self.mat[xy[1]][xy[0]] = Grid(Wall())

	def show(self):
		mat = [[self.mat[y][x].block.char for x in xrange(self.width)] for y in xrange(self.height)]
		lines = [''.join(mat[y]) for y in xrange(self.height)]
		return '\n'.join(lines)

















