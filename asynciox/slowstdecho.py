import asyncio
import os
import sys
import logging

log = logging.getLogger(__name__)
D = log.debug
import signal
import atexit


class App:
    def __init__(self):
        self.done = False

    async def open(self, loop):
        self.stdin = asyncio.StreamReader()
        _, self.stdin_proto = await loop.connect_read_pipe(
            lambda: asyncio.StreamReaderProtocol(self.stdin),
            # helper proto for reader
            sys.stdin)
        trans, proto = await loop.connect_write_pipe(
            asyncio.streams.FlowControlMixin,  # implements .drain() for writer
            sys.stdout
            # os.fdopen(1,'wb')
        )
        self.stdout = asyncio.StreamWriter(trans, proto,
                                           None,  # no attached reader
                                           loop)

    def close(self):
        self.done = True

    async def run(self):
        D("run")
        while not self.done:
            line = await self.stdin.readline()
            await asyncio.sleep(1.0)
            D(line)
            self.stdout.write(line)
            await self.stdout.drain() # !!! raises ConnectionLost
        self.stdin.feed_eof()
        self.stdout.close()
        D("app done")


def main():
    app = App()

    # setup main event loop
    loop = asyncio.get_event_loop()

    def stop():
        app.close()
        loop.stop()

    loop.add_signal_handler(signal.SIGTERM, stop)
    loop.add_signal_handler(signal.SIGINT, stop)
    # python bug http://bugs.python.org/issue23548
    atexit.register(asyncio.get_event_loop().close)

    loop.run_until_complete(app.open(loop))
    asyncio.ensure_future(app.run())
    loop.run_forever()
    D("main done")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
