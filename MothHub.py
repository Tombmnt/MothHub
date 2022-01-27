#!/usr/bin/env python
# Base template from https://gist.github.com/opie4624/3896526 

import argparse, logging
from colorama import init as colorama_init
from handlers.data_handler import Data_Handler

from socket_server import Socket_Server

def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    log = logging.getLogger(__name__)

    database_service = Database_Service("hubDB")

    sock_srv = Socket_Server(database_service)
    # The server starts itself and locks this thread, we're done here until it exits.

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
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    # Setup colorama for pretty prints
    colorama_init(autoreset=True)

    main(args, loglevel)