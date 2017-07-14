#!/usr/bin/python3

# https://github.com/cmanaha/python-elasticsearch-logger

import logging
import asyncio

from cmreslogging.handlers import CMRESHandler

log = logging.getLogger(__name__)

async def main():
    log.debug("this is a debugging message")
    log.info("this is an informational message")
    log.warning("this is a warning message")
    log.error("this is an error message")
    log.critical("this is a critical message")
    # extra log event based information
    log.info("informational message with extra info",
             extra={
                 "extra_key": "extra_value",
             })


def setup_logging():
    logging.basicConfig(level=logging.DEBUG)
    handler = CMRESHandler(
        hosts=[
            {"host": "localhost", "port": 9200},
        ],
        auth_type=CMRESHandler.AuthType.NO_AUTH,
        es_index_name="my_python_index",
        es_additional_fields={
          "app": "eslogs1",
        },
    )
    root_log = logging.getLogger()
    root_log.setLevel(logging.DEBUG)
    root_log.addHandler(handler)


if __name__ == "__main__":
    setup_logging()
    asyncio.get_event_loop().run_until_complete(main())
