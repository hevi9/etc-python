#!/usr/bin/python3

import logging
import coloredlogs
import asyncio

log = logging.getLogger(__name__)

async def main():
    log.debug("this is a debugging message")
    log.info("this is an informational message")
    log.warning("this is a warning message")
    log.error("this is an error message")
    log.critical("this is a critical message")

if __name__ == "__main__":
    coloredlogs.install(level="DEBUG")
    asyncio.get_event_loop().run_until_complete(main())
