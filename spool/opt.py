import logging

log = logging.getLogger(__name__)


def main():
    lengths = [
        1.0,
        2.2,
        3.1,
    ]
    for width in [0.0, 6.5, 9.0]:
        log.info("")
        for length in lengths:
            log.info(
                "%f %f %f %f",
                width,
                length,
                width / length,
                width % length,
            )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
