#!/usr/bin/env python
# Base template from https://gist.github.com/opie4624/3896526 

import argparse, logging
from datetime import datetime, timedelta
from typing import Dict
from colorama import init as colorama_init
from database_service import Database_Service

from socket_server import Socket_Server

# These functions are for debugging and not for using for anything useful
def print_cbk(new_data: Dict):
    print(f"New data on test db: {new_data}")

def test_db(db: Database_Service):
    db.insert_data("test", {"key1":"value1", "key2":1234})

    db.register_callback("test", print_cbk)
    db.insert_data("test", {"key3":"value1", "key4":"Hello WORLD!"})

    db.unregister_callback("test", print_cbk)
    db.insert_data("test", {"key5":"value999", "key6":42})

    data = db.obtain_data("test", datetime.now() - timedelta(seconds=20), datetime.now())
    print(data)
# ---- End -----

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