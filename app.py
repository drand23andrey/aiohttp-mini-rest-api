from aiohttp import web
import json

async def handle(request):
       
    #загрузить из json
    with open('news.json', 'r', encoding='utf-8') as ns: #открываем файл на чтение
        news = json.load(ns) #загружаем из файла данные в словарь news
    #загрузить из json
    with open('comments.json', 'r', encoding='utf-8') as cs: #открываем файл на чтение
        comments = json.load(cs) #загружаем из файла данные в словарь comments

    news_list = news.get('news')

    comments_count = 0
    for new in news_list:
        id = new.get('id')

    response_obj = s

    return web.Response(text=json.dumps(response_obj))
    
async def news_id(request):

    id = request.match_info['id']

    #загрузить из json
    with open('news.json', 'r', encoding='utf-8') as ns: #открываем файл на чтение
        news = json.load(ns) #загружаем из файла данные в словарь news
    #загрузить из json
    with open('comments.json', 'r', encoding='utf-8') as cs: #открываем файл на чтение
        comments = json.load(cs) #загружаем из файла данные в словарь comments

    response_obj = comments

    return web.Response(text=json.dumps(response_obj))

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/news/{id}', news_id)


web.run_app(app)