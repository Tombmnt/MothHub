#!/usr/bin/env python
# Base template from https://gist.github.com/opie4624/3896526 

import argparse, logging, sys
from colorama import init as colorama_init
from handlers.data_handler import Data_Handler
from modules.lora import LoRaE5, Regions, Modes

from socket_server import Socket_Server

def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  log = logging.getLogger(__name__)

  data_handler = Data_Handler()
  sock_srv = Socket_Server(data_handler)

  #TODO: move this out of here
  if(sys.platform.startswith("win")):
    lora_port = "COM6" # TODO: Discover the right port (Very likely to be whatever.... #windows)
  else:
    lora_port = "/dev/ttyUSB0" # TODO: Discover the right port (very likely to be ttyUSB0)

  lora_shore = LoRaE5(lora_port, Regions.america, Modes.transmit, None)

def debug_loop_send_lora_data(lora_device):
    input_str = ""
    while(input_str != "quit"):
        input_str = input("Send data ('quit' to stop): ")
        lora_device.send_string(input_str)

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