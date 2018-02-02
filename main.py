#!/usr/bin/env python
import os
from tornado import web
import tornado.wsgi

from handlers import *

app = web.Application(
    handlers=[(r"/", IndexHandler)],
    template_path=os.path.join(os.path.dirname(__file__), "templates"))
app = tornado.wsgi.WSGIAdapter(app)
