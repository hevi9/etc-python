import asyncio
import logging

import sys

log = logging.getLogger(__name__)
D = log.debug

async def aio_stdin(*, loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    stdin = asyncio.StreamReader(loop=loop)
    await loop.connect_read_pipe(
        lambda: asyncio.StreamReaderProtocol(stdin),
        sys.stdin
    )
    return stdin

async def ticker():
    for _ in range(10):
        await asyncio.sleep(1)
        print("TICK")

async def main():
    stdin = await aio_stdin()
    for _ in range(4):
        line = await stdin.readline()
        print("LINE", line)
    D("main done")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.get_event_loop().set_debug(True)
    asyncio.get_event_loop().run_until_complete(asyncio.wait([
            main(), ticker()
        ]))
