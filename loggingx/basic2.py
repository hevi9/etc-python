import logging
import json
from json.encoder import JSONEncoder
import asyncio
from aiohttp.web import Application, Response, MsgType, WebSocketResponse


class JSONEncoderEx(JSONEncoder):

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

    def default(self, o):
        return repr(o)


class WSHandler(logging.Handler):

    def __init__(self):
        super().__init__()

    def emit(self, record):
        print(json.dumps(record.__dict__, cls=JSONEncoderEx))


def test():
    log = logging.getLogger()
    log.debug("debug test")
    log.info("info test")
    log.warning("warning test")
    log.error("error test")
    try:
        1 / 0
    except:
        log.exception("exception test")
    log.critical('critical test')


def main():
    loop = asyncio.get_event_loop()

    app = Application(loop=loop)

    log = logging.getLogger()
    log.addHandler(WSHandler())
    log.setLevel(logging.DEBUG)

    test()

if __name__ == "__main__":
    main()
