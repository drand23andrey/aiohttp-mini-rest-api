# -*- coding: utf-8 -*-

# юнитетесты для функций api

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from aiohttp_mini_rest_api import handle, find_news_by_id

class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        app = web.Application()
        app.router.add_get('/', handle)
        app.router.add_get('/news/{id}', find_news_by_id)
        return app

    # проверка find_news_by_id() на запрос "равильной" новости
    @unittest_run_loop
    async def test_find(self):
        resp = await self.client.request("GET", "/news/2")
        assert resp.status == 200
        text = await resp.text()
        assert '{"id": 2, "title": "news_2", "date": "2019-01-01T21:56:35", "body": "The news", "deleted": false, ' \
               '"comments": [{"id": 2, "news_id": 2, "title": "comment_2", "date": "2019-01-02T21:58:25", "comment": ' \
               '"Comment"}], "comments_count": 1}' == text
        
    # проверка find_news_by_id() на запрос несуществующей новости (не существующий id)
    @unittest_run_loop
    async def test_find_id(self):
        resp = await self.client.request("GET", "/news/0")
        assert resp.status == 200
        text = await resp.text()
        assert '404: Not Found' == text

    # проверка find_news_by_id() на запрос deleted новости (новость id==3 точно deleted)
    @unittest_run_loop
    async def test_find_deleted(self):
        resp = await self.client.request("GET", "/news/3")
        assert resp.status == 200
        text = await resp.text()
        assert '404: Not Found' == text

    # проверка find_news_by_id() на запрос новости, время которой еще не пришло
    @unittest_run_loop
    async def test_find_coming_soon(self):
        resp = await self.client.request("GET", "/news/4")
        assert resp.status == 200
        text = await resp.text()
        assert '404: Not Found' == text    

    # проверка всех условий функции handle() одновременно
    @unittest_run_loop
    async def test_handler(self):
        resp = await self.client.request("GET", "/")
        assert resp.status == 200
        text = await resp.text()
        assert '{"news": [{"id": 2, "title": "news_2", "date": "2019-01-01T21:56:35", "body": "The news", "deleted": ' \
               'false, "comments_count": 1}, {"id": 6, "title": "news_2", "date": "2019-03-01T21:56:35", "body": ' \
               '"The news", "deleted": false, "comments_count": 0}, {"id": 7, "title": "news_2", "date": "2019-0' \
               '3-01T21:57:35", "body": "The news", "deleted": false, "comments_count": 0}], "news_count": 3}' == text
