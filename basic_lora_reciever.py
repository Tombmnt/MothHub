#!/usr/bin/env python
# Base template from https://gist.github.com/opie4624/3896526 

import argparse, logging
from colorama import init as colorama_init
from modules.lora import LoRaE5, Regions, Modes

localhost = "127.0.0.1"

def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    log = logging.getLogger(__name__)

    lora_device = LoRaE5(args.comm[0], Regions.america, Modes.recieve, print_recieved, is_on_pi=False)

    input("Press any key to quit...\n")

def print_recieved(data):
    logging.info("Recieved data from LoRa :\n"+str(data))

# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "TODO")
    # TODO Specify your real parameters here.
    parser.add_argument(
                        "-v",
                        "--verbose",
                        help="increase output verbosity",
                        action="store_true")
    parser.add_argument(
                        "-c",
                        "--comm",
                        nargs='+',
                        help="Comm port of the LoRa device to use"
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