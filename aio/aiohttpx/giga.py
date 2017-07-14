import asyncio
from aiohttp import web
import logging
log = logging.getLogger(__name__)
D = log.debug


@asyncio.coroutine
def handle(request):
    chars = 2 ** 6
    chunk = "".join(chr(i) for i in range(0x21, 0x21 + chars)).encode("utf8")
    n = int(2 ** 24 / chars)
    resp = web.StreamResponse()
    resp.content_length = n * chars
    resp.start(request)
    D("start write")
    for i in range(n):
        if not i % 10000:
            D("step %i", i)
        resp.write(chunk)
        yield from resp.drain()
    yield from resp.write_eof()
    D("end write")
    return resp



@asyncio.coroutine
def handle2(request):
    chars = 2 ** 6
    chunk = "".join(chr(i) for i in range(0x21, 0x21 + chars)).encode("utf8")
    n = int(2 ** 24 / chars)
    resp = web.StreamResponse()
    resp.content_length = n * chars
    resp.start(request)
    D("start write")
    for i in range(n):
        if not i % 10000:
            D("step %i", i)
        resp.write(chunk)
        yield from resp.drain()
        yield from asyncio.sleep(0)
    yield from resp.write_eof()
    D("end write")
    return resp


@asyncio.coroutine
def handle_nowrite2(request):
    chars = 2 ** 6
    chunk = "".join(chr(i) for i in range(0x21, 0x21 + chars)).encode("utf8")
    n = int(2 ** 24 / chars)
    resp = web.StreamResponse()
    resp.content_length = n * chars
    resp.start(request)
    D("start write")
    for i in range(n):
        if not i % 10000:
            D("step %i", i)
        #resp.write(chunk)
        #yield from resp.drain()
    yield from resp.write_eof()
    D("end write")
    return resp



@asyncio.coroutine
def handle_nowrite(request):
    resp = web.StreamResponse()
    resp.start(request)
    D("start write %s", request)
    for i in range(5):
        yield from asyncio.sleep(1)
        D("step %i", i)
    yield from resp.write_eof()
    D("end write")
    return resp


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', handle2)

    srv = yield from loop.create_server(app.make_handler(),
                                        '127.0.0.1', 8081)
    print("Server started at http://127.0.0.1:8081")
    return srv


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
