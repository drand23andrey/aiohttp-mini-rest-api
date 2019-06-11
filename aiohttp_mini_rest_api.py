# -*- coding: utf-8 -*-

from aiohttp import web
import json
from datetime import datetime


# вернет значение подходящий по id комментов
def get_comments_count(new_id, comments):
    comments_count = 0
        
    for comment_dict in comments:
        news_id = comment_dict.get('news_id')
        if news_id == new_id:
            comments_count += 1
    
    return comments_count


# вернет список комментов, каждый из которых - словарь
def get_comments_by_id(id, comments):
    ret_comments_list = []
    
    for comment_dict in comments:
        news_id = comment_dict.get('news_id')
        if news_id == id:
            ret_comments_list.append(comment_dict)
            ret_comments_list = sorted(ret_comments_list, key = lambda n: n['date'])
    
    return ret_comments_list


# по заданию GET '/'
async def handle(request):
       
    # загрузить из json
    with open('news.json', 'r', encoding='utf-8') as ns:    # открываем файл на чтение
        news_dict = json.load(ns)                           # загружаем из файла данные в словарь news
    # загрузить из json
    with open('comments.json', 'r', encoding='utf-8') as cs:    # открываем файл на чтение
        comments_dict = json.load(cs)                           # загружаем из файла данные в словарь comments

    news = news_dict.get('news')
    comments = comments_dict.get('comments')

    ret_news_dict = {'news': [], 'news_count': 0} 

    for new_dict in news:
        # не возвращаем новость которая удалена или время публикации новости еще не пришло
        if new_dict.get('deleted') or datetime.now().strftime("%Y-%m-%dT%H:%M:%S") < new_dict.get('date'):
            continue

        id = new_dict.get('id')
        new_dict['comments_count'] = get_comments_count(id, comments)

        ret_news_dict['news'].append(new_dict)
        ret_news_dict['news_count'] += 1

    ret_news_dict['news'] = sorted(ret_news_dict['news'], key = lambda n: n['date'])

    return web.Response(text=json.dumps(ret_news_dict))
    


# по заданию GET '/news/{id}'
async def find_news_by_id(request):

    # id из запроса GET/news/{id}
    id = int(request.match_info['id'])

    # загрузить из json
    with open('news.json', 'r', encoding='utf-8') as ns:    # открываем файл на чтение
        news_dict = json.load(ns)                           # загружаем из файла данные в словарь news
    # загрузить из json
    with open('comments.json', 'r', encoding='utf-8') as cs:    # открываем файл на чтение
        comments_dict = json.load(cs)                           # загружаем из файла данные в словарь comments

    news = news_dict.get('news')
    comments = comments_dict.get('comments')

    ret_news_dict = {}

    for new_dict in news: 
        new_id = new_dict.get('id')
        if new_id == id:
            ret_news_dict = new_dict
            ret_news_dict['comments'] = get_comments_by_id(id, comments)
            ret_news_dict['comments_count'] = get_comments_count(id, comments)
            break

    # вернем 404 при выполнении одного из условий из задания
    if (not ret_news_dict) or ret_news_dict['deleted'] or datetime.now().strftime("%Y-%m-%dT%H:%M:%S") < new_dict.get('date'):
        # raise web.HTTPFound('/')
        return web.Response(text='404: Not Found')

    return web.Response(text=json.dumps(ret_news_dict))
