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

import copy
import random

from core.dungeon.base import (
	GeneratorBase,
	Room,
)

class Generator(GeneratorBase):
	def __init__(self, width=64, height=64, max_rooms=15, min_room_xy=5, max_room_xy=10, rooms_overlap=False, random_connections=1, random_spurs=3, **kwargs):
		super(Generator, self).__init__()

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

	def _getMinRoom(self):
		x = random.randint(1, (self.width - self.min_room_xy - 1)) # edge is wall
		y = random.randint(1, (self.height - self.min_room_xy - 1))
		return Room(x, y, self.min_room_xy, self.min_room_xy)

	def _isOverlapping(self, room):
		for r in self.room_list:
			if r.overlapping(room):
				return True
		return False

	def _joinRooms(self, room1, room2):
		x_overlap = y_overlap = False
		if not (room2.right < room1.x or room1.right < room2.x):
			x_overlap = True
		if not (room2.top < room1.y or room1.top < room2.y):
			y_overlap = True

		xs = sorted([room1.left, room2.left, room1.right, room2.right])
		ys = sorted([room1.bottom, room2.bottom, room1.top, room2.top])
		if x_overlap:
			x = random.randint(max(room1.left, room2.left), min(room1.right, room2.right))
			self.corridor_list.append(Room(x, ys[1], 1, ys[2] - ys[1]))

		elif y_overlap:
			y = random.randint(max(room1.bottom, room2.bottom), min(room1.top, room2.top))
			self.corridor_list.append(Room(xs[1], y, xs[2] - xs[1], 1))

		else:
			ro = [room1, room2]
			# random.shuffle(ro) # avoid road side-by-side
			x = random.randint(ro[0].left, ro[0].right)
			if ro[0].top < ro[1].top: # r0 down
				h = random.randint(ro[1].bottom - ro[0].top, ro[1].top - ro[0].top)
				self.corridor_list.append(Room(x, ro[0].top + 1, 1, h))
				if ro[1].right < x: # left
					w = x - ro[1].right
					self.corridor_list.append(Room(ro[1].right + 1, ro[0].top + h, w, 1))
				else:
					w = ro[1].left - x
					self.corridor_list.append(Room(x, ro[0].top + h, w, 1))
			else: # r0 up
				h = random.randint(ro[0].bottom - ro[1].top, ro[0].bottom - ro[1].bottom)
				self.corridor_list.append(Room(x, ro[0].bottom - h, 1, h))
				if ro[1].right < x: # left
					w = x - ro[1].right
					self.corridor_list.append(Room(ro[1].right + 1, ro[0].bottom - h, w, 1))
				else:
					w = ro[1].left - x
					self.corridor_list.append(Room(x, ro[0].bottom - h, w, 1))

	
	def _fillGrid(self, grids, room, block):
		for x in xrange(room.left, room.right + 1):
			for y in xrange(room.bottom, room.top + 1):
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

		# build no overlap rooms
		rooms = []
		x, y = 1, 1
		while x < self.width:
			y = 1
			while y < self.height:
				room = Room(x, y, self.min_room_xy, self.min_room_xy)
				if not (room.right >= self.width or room.top >= self.height or self._isOverlapping(room)):
					rooms.append(room)
				y += self.min_room_xy
			x += 1

		# print len(rooms)
		# TODO
		for room in rooms:
			if not self._isOverlapping(room):
				# room = Room(room.x, room.y, random.randint(self.min_room_xy, room.w), random.randint(self.min_room_xy, room.h))
				self.room_list.append(room)
				if len(self.room_list) >= self.max_rooms:
					break

		if len(self.room_list) == 1:
			return

		# connect rooms
		for i in xrange(len(self.room_list) - 1):
			self._joinRooms(self.room_list[i], self.room_list[i + 1])

		# random connect rooms
		id_list = range(len(self.room_list))
		for i in xrange(self.random_connections):
			id1, id2 = random.sample(id_list, 2)
			if abs(id1 - id2) == 1: # existed connect road
				continue
			self._joinRooms(self.room_list[id1], self.room_list[id2])

		# output
		from core.grid import GridsMatrix
		from core import block

		ret = GridsMatrix(self.width, self.height)
		for i, room in enumerate(self.room_list):
			self._fillGrid(ret, room, block.Road(i))

		for room in self.corridor_list:
			self._fillGrid(ret, room, block.Road())

		ret.wrapWall()
		return ret

	def getRooms(self):
		return (self.room_list, self.corridor_list)










