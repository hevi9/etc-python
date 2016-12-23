import asyncio
import logging
import asyncio.unix_events
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


# XXX <_UnixWritePipeTransport fd=1 idle bufsize=0> was closed by peer
# https://github.com/python/asyncio/issues/369
# when there is stdin activity TTY seems to close stdout
async def aio_stdout(*, loop=None):
    if loop is None:
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
    stdin = await aio_stdin()
    stdout = await aio_stdout()
    for _ in range(4):
        data = await stdin.readline()
        stdout.write(data)
        # await stdout.drain()
    D("main done")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.get_event_loop().set_debug(True)
    asyncio.get_event_loop().run_until_complete(asyncio.wait([
            main()
        ]))
