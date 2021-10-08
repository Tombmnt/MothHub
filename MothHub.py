#!/usr/bin/env python
# Base template from https://gist.github.com/opie4624/3896526 

# import modules used here --sys is a very standard one
from os import read
import sys, argparse, logging, json

def main(args, loglevel):
  logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
  
  # TODO Replace this with your actual code.
  print("Hello there.")
 

def loadModules(configfile):
    logging.debug("Loading modules from "+configfile)

    modules = None

    with open(configfile) as json_file:
        data = json.load(json_file)
        for m in data['modules']:
            logging.info("Loading: " + m["name"])
            logging.debug("From: " + m["path"])



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
  
  main(args, loglevel)