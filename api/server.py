# -*- coding: utf-8 -*-
#
# Copyright 2016 HuangWei
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

import sys
sys.path.append('../')

import signal

import tornado.ioloop
import tornado.web

from core import dungeon

class DungeonsHandler(tornado.web.RequestHandler):
	def get(self):
		modname = self.get_argument('mod')
		w = int(self.get_argument('w', 128))
		h = int(self.get_argument('h', 128))
		kwargs = {k: vl[0] for k, vl in self.request.arguments.iteritems()}
		kwargs.pop('mod', None)
		kwargs.pop('w', None)
		kwargs.pop('h', None)

		obj = dungeon.newGenerator(modname, w, h, kwargs)
		obj.generate()


def main():
	application = tornado.web.Application([
		(r"/dungeons", DungeonsHandler),
	],
	debug=True, autoreload=True, serve_traceback=True)

	application.listen(8181)
	print 'server listen...'

	ioloop = tornado.ioloop.IOLoop.current()
	signal.signal(signal.SIGINT, lambda sig, frame: ioloop.add_callback_from_signal(ioloop.stop))
	signal.signal(signal.SIGTERM, lambda sig, frame: ioloop.add_callback_from_signal(ioloop.stop))

	ioloop.start()
	print 'server stop'

if __name__ == '__main__':
	main()

	