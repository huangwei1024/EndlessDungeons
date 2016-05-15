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

import tornado.ioloop
import tornado.web

class CreateHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, world")


def main():
	application = tornado.web.Application([
		(r"/create", CreateHandler),
	])
	application.listen(8181)
	tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
	main()

	