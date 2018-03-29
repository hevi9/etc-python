import random

from eslog import log
from eslog import targets, adds

INF = 10
STP = 5
DBG = -10


def run():
    log(INF, "Items are", 99, False)
    for index in range(5):
        log(STP, "Round", index, result=random.random())
    log(INF, "done")


def main():
    log.setup(
        adds.add_location,
        # targets.target_pprint,
        # targets.target_console_json,
        # targets.target_console,
    )
    log.level = STP
    run()


if __name__ == "__main__":
    main()
