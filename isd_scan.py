#!/usr/bin/env python
#######################################################################
# Internet Scan Data Searcher                                         #
#######################################################################
# Copyright (C) 2015 Silas Cutler   <Silas.Cutler@Gmail.com>          #
#######################################################################
# This file is subject to the terms and conditions of the BSD License.#
#######################################################################

import argparse
from lib.functions import *

# Main
def main():
	parser, args = parse_args()

	if args.add_rule and args.rule_name and args.scan_regex:
		add_rule( args.rule_name, args.scan_regex )
	elif args.list_rules:
		list_rule()
	elif args.file:
		if args.scan_regex:
			single_scan(args.file, args.scan_regex)
		elif args.rule_name:
			scan_full(args.file, args.rule_name)
		else:
			scan_full(args.file)
	else:
		parser.print_help()	

# Parse arguments 
# IN:
# OUT: ArgumentParser, parsed_args
def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", help="Path to file", metavar="FILE")


	parser.add_argument("-l", "--list_rules", help="List rules", action="store_true")

	
	parser.add_argument("-a", "--add_rule", help="Add Scan rule to match", action="store_true")
	parser.add_argument("-n", "--rule_name", help="Name for Rule")
	parser.add_argument("-r", "--scan_regex", help="Regex to match against data")
	return parser, parser.parse_args()

if __name__ == "__main__":
	main()

