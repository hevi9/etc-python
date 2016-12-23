import asyncio
import logging

import sys

log = logging.getLogger(__name__)
D = log.debug

async def aio_stdout():
    loop = asyncio.get_event_loop()
    trans, proto = await loop.connect_write_pipe(
        asyncio.streams.FlowControlMixin,  # implements .drain() for writer
        sys.stdout
    )
    stdout = asyncio.StreamWriter(
        trans, proto,
        None,  # no attached reader
        loop)
    return stdout

async def main():
    stdout = await aio_stdout()
    # stdout = sys.stdout.buffer

    # write
    stdout.write("test1\n".encode())
    stdout.write("test2\n".encode())
    stdout.write("test3\n".encode())
    print("test4")
    await stdout.drain()

    # finish
    stdout.close()
    D("main done")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.get_event_loop().set_debug(True)
    asyncio.get_event_loop().run_until_complete(main())
