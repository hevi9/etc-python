import asyncio
import logging
import bluetooth
from time import monotonic as clock

log = logging.getLogger(__name__)

MAC = "B8:08:D7:17:13:0E"
FREQUENCY = 5
MAYBE_DURATION = 20


async def poll_bt_mac(mac, frequency, logic):
    loop = asyncio.get_event_loop()

    while True:
        start_time = clock()
        name = await loop.run_in_executor(
            None,
            bluetooth.lookup_name,
            mac,
            frequency
        )
        if name:
            logic.on_found(name)
        else:
            logic.on_not_found()
        wait_time = clock() - start_time
        await asyncio.sleep(max(0, frequency - wait_time))
        log.debug(
            "lookup_name(%r) -> %r, lookup_time=%.3fs frequency_time=%.3fs",
            MAC,
            name,
            wait_time,
            clock() - start_time,
        )


class Timeout:
    def __init__(self, duration):
        self._duration = duration
        self._set_time = clock()

    def __bool__(self):
        return clock() - self._set_time > self._duration

    def reset(self):
        self._set_time = clock()


# noinspection PyCallByClass,PyTypeChecker
class Logic:
    class State:
        def on_found(self, name):
            pass

        def on_not_found(self):
            pass

    # noinspection PyUnresolvedReferences
    class AWAY(State):
        def on_found(self, name):
            self.timeout.reset()
            self.transit(Logic.AWAY_MAYBE)

    # noinspection PyUnresolvedReferences
    class AWAY_MAYBE(State):
        def on_not_found(self):
            self.transit(Logic.AWAY)

        def on_found(self, name):
            if self.timeout:
                # signal out HERE really
                self.transit(Logic.HERE)

    # noinspection PyUnresolvedReferences
    class HERE(State):
        def on_not_found(self):
            self.timeout.reset()
            self.transit(Logic.HERE_MAYBE)

    # noinspection PyUnresolvedReferences
    class HERE_MAYBE(State):
        def on_found(self, name):
            self.transit(Logic.HERE)

        def on_not_found(self):
            if self.timeout:
                # signal out AWAY really
                self.transit(Logic.AWAY)

    def __init__(self):
        self._state = Logic.AWAY
        self.timeout = Timeout(10)

    def on_found(self, name):
        self._state.on_found(self, name)

    def on_not_found(self):
        self._state.on_not_found(self)

    def transit(self, state):
        log.info(
            "%s => %s",
            self._state.__name__,
            state.__name__,
        )
        self._state = state


async def main():
    logic = Logic()
    await poll_bt_mac(MAC, FREQUENCY, logic)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.get_event_loop().run_until_complete(main())
