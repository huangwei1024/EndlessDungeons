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

import os

def newGenerator(modname, width, height, kwargs):
	g = globals()
	# if hasattr(g, modname):
	# 	mod = getattr(g, modname)
	# 	modpath = mod.__file__
	# 	print mod, 'existed, reload', modpath
	# 	if modpath.endswith('.py'):
	# 		try:
	# 			os.remove(modpath + 'c')
	# 		except Exception, e:
	# 			pass
	# 		try:
	# 			os.remove(modpath + 'o')
	# 		except Exception, e:
	# 			pass
	# 	else:
	# 		try:
	# 			os.remove(modpath)
	# 		except Exception, e:
	# 			pass
	# 	delattr(g, modname)

	mod = __import__(modname, g)
	cls = mod.Generator
	obj = cls(width=width, height=height, **kwargs)
	return obj