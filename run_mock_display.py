#!/usr/bin/env python
# Base template from https://gist.github.com/opie4624/3896526 

import argparse, logging
import threading
from colorama import init as colorama_init
from modules.mock.mock_display import MockDisplay

localhost = "127.0.0.1"

def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    log = logging.getLogger(__name__)

    mock_display = MockDisplay(320, 240, args.name[0], localhost)
    mock_display.run()


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "TODO")
    # TODO Specify your real parameters here.
    parser.add_argument(
                        "-v",
                        "--verbose",
                        help="increase output verbosity",
                        action="store_true")
    parser.add_argument(
                        "-n",
                        "--name",
                        nargs='+',
                        help="Name of the started screen"
    )
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    # Setup colorama for pretty prints
    colorama_init(autoreset=True)

    main(args, loglevel)