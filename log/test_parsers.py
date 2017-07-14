from mkwww.parsers import Parser
from mkwww import LOG, LOG_DEEP
from texts import *


def ntest_Parser_01():

    parser = Parser()
    parser.parse_text(text_04)

if __name__ == "__main__":
    import logging.config
    logging.basicConfig()
    logging.config.dictConfig({
        "version": 1,
        # "disable_existing_loggers": False,
        # "incremental": True,
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        "loggers": {
            "": {
                "level": "DEBUG"
            },
            LOG: {
                'handlers': ['default'],
                "level": "DEBUG",
                'propagate': False
            },
            LOG_DEEP: {
                'handlers': ['default'],
                "level": "DEBUG",
                'propagate': False
            }

        }
    })
    # logging.basicConfig()
    ntest_Parser_01()
