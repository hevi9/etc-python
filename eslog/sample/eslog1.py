import random

from eslog import log
from eslog import processors

INF = 10
STP = 5
DBG = -10


def main1():
    log.setup(
        # processors.add_location,
        processors.target_pprint,
    )
    log.level = INF
    log(INF, "Items are", 99, False)
    for index in range(5):
        log(INF, "Round", index, result=random.random())
    log(INF, "done")


if __name__ == "__main__":
    main1()
