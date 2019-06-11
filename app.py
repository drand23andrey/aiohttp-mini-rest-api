# -*- coding: utf-8 -*-

from aiohttp import web
import json
from datetime import datetime
import aiohttp_mini_rest_api


app = web.Application()
app.router.add_get('/', aiohttp_mini_rest_api.handle)
app.router.add_get('/news/{id}', aiohttp_mini_rest_api.find_news_by_id)

web.run_app(app)