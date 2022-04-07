#! /usr/bin/env python3
import time
import logging

from modules.gameloop import where
from modules.platform import win


log = logging.getLogger(__name__)


def main():
    log.info("start")
    while True:
        log.info("Loop")
        try:
            if win.find_game():
                where()
        except Exception as error:
            log.error("Error: %s", error)
            time.sleep(1)


if __name__ == "__main__":
    main()
