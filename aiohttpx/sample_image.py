# paste from http://aiohttp.readthedocs.org/en/v0.14.4/

import asyncio
from aiohttp import web
import logging
import mimetypes


@asyncio.coroutine
def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(body=text.encode('utf-8'))


@asyncio.coroutine
def image_handle(request):
    name = request.match_info.get('name', "Anonymous")
    path = "sample.jpeg"
    content_type, encoding = mimetypes.guess_type(path)
    with open(path,"rb") as fo:
        data = fo.read()    
    return web.Response(body=data, content_type=content_type)


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', image_handle)
    app.router.add_route('GET', '/{name}', handle)

    srv = yield from loop.create_server(app.make_handler(),
                                        '127.0.0.1', 8081)
    print("Server started at http://127.0.0.1:8081")
    return srv


logging.basicConfig(level=logging.DEBUG)
loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass