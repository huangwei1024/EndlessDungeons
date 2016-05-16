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

# algorithm like
# http://www.roguebasin.com/index.php?title=A_Simple_Dungeon_Generator_for_Python_2_or_3

from __future__ import absolute_import

import random
from collections import namedtuple

Room = namedtuple('Room', ('x', 'y', 'w', 'h'))

class Generator(object):
	def __init__(self, width=64, height=64, max_rooms=15, min_room_xy=5, max_room_xy=10, rooms_overlap=False, random_connections=1, random_spurs=3, **kwargs):
		self.width = width
		self.height = height
		self.max_rooms = max_rooms
		self.min_room_xy = min_room_xy
		self.max_room_xy = max_room_xy
		self.rooms_overlap = rooms_overlap
		self.random_connections = random_connections
		self.random_spurs = random_spurs
		
		self.room_list = []
		self.corridor_list = []

	def _getRoom(self):
		w = random.randint(self.min_room_xy, self.max_room_xy)
		h = random.randint(self.min_room_xy, self.max_room_xy)
		x = random.randint(1, (self.width - w - 1)) # edge is wall
		y = random.randint(1, (self.height - h - 1))
		return Room(x, y, w, h)

	def _isOverlapping(self, room):
		for r in self.room_list:
			if not ((r.x + r.w < room.x or room.x + room.w < r.x) and (r.y + r.h < room.y or room.y + room.h < r.y)):
				return True
		return False

	def _joinRooms(self, room1, room2):
		x_overlap = y_overlap = False
		if not (room2.x + room2.w < room1.x or room1.x + room1.w < room2.x):
			x_overlap = True
		if not (room2.y + room2.h < room1.y or room1.y + room1.h < room2.y):
			y_overlap = True
	
	def _fillGrid(self, grids, room, block):
		for x in xrange(room.x, room.x + room.w + 1):
			for y in xrange(room.y, room.y + room.h + 1):
				grids.set(x, y, block)

	def generate(self):
		# build rooms
		for i in xrange(self.max_rooms * 5):
			room = self._getRoom()
			if self.rooms_overlap or len(self.room_list) == 0:
				self.room_list.append(room)
			else:
				if not self._isOverlapping(room):
					self.room_list.append(room)

			if len(self.room_list) >= self.max_rooms:
				break

		if len(self.room_list) == 1:
			return

		# connect rooms
		for i in xrange(len(self.room_list) - 1):
			self._joinRooms(self.room_list[i], self.room_list[i + 1])

		# random connect rooms
		for i in xrange(self.random_connections):
			room1, room2 = random.sample(self.room_list, 2)
			self._joinRooms(room1, room2)

		# output
		from core.grid import GridsMatrix
		from core import block

		ret = GridsMatrix(self.width, self.height)
		for room in self.room_list:
			self._fillGrid(ret, room, block.Road())

		for room in self.corridor_list:
			self._fillGrid(ret, room, block.Road())

		ret.wrapWall()
		return ret












