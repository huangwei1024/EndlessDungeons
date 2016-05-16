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

StrConvList = [
	lambda s: None if len(s) == 0 else 1/0,
	lambda s: int(s),
	lambda s: float(s),
	lambda s: s[1:-1] if s[0] == '\'' and s[0] == '"' else 1/0,
	lambda s: s[1:-1].split(',') if s[0] == '[' and s[-1] == ']' else 1/0,
]

def convertStrDict(d):
	ret = {}
	for k, v in d.iteritems():
		vv = v
		try:
			sv = v.replace(';', '').replace(' ', '').replace('\t', '').replace('\n', '')
			vv = eval(sv, {}, {})
		except:
			pass
		# print type(v), v, type(vv), vv
		ret[k] = vv
	print ret
	return ret

def ascii2html(s):
	return s
	# return s.replace('\n', '<br/>\n').replace(' ', '&nbsp;')

class DungeonsHandler(tornado.web.RequestHandler):
	def get(self):
		kwargs = {k: vl[0] for k, vl in self.request.arguments.iteritems()}
		kwargs = convertStrDict(kwargs)

		modname = kwargs.pop('mod', 'simple')
		w = kwargs.pop('w', 64)
		h = kwargs.pop('h', 64)
		show = kwargs.pop('show', True)

		obj = dungeon.newGenerator(modname, w, h, kwargs)
		grids = obj.generate()
		if show:
			self.render('dungeons.html', map=ascii2html(grids.show()), mod=modname, width=w, height=h, kwargs=kwargs)
		else:
			self.write(grids.show())


def main():
	application = tornado.web.Application([
		(r"/dungeons", DungeonsHandler),
	],
	debug=True,
	autoreload=True,
	serve_traceback=True,
	static_path='../static/',
	template_path='../static/template/')

	application.listen(8181)
	print 'server listen...'

	ioloop = tornado.ioloop.IOLoop.current()
	signal.signal(signal.SIGINT, lambda sig, frame: ioloop.add_callback_from_signal(ioloop.stop))
	signal.signal(signal.SIGTERM, lambda sig, frame: ioloop.add_callback_from_signal(ioloop.stop))

	ioloop.start()
	print 'server stop'

if __name__ == '__main__':
	main()

	