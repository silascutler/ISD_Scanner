#!/usr/bin/env python
#######################################################################
# Internet Scan Data Searcher                                         #
#######################################################################
# Copyright (C) 2015 Silas Cutler   <Silas.Cutler@Gmail.com>          #
#######################################################################
# This file is subject to the terms and conditions of the BSD License.#
#######################################################################

import re
import sys
import json
import gevent
import gzip
import resource
import base64
from database import *
from gevent.select import select
from gevent.pool import Pool

class ISD_Scanner(object):
	# Init Scanner Class
	# IN:
	# OUT: 
	def __init__(self,r_file, d_ruleset):
		self.pool = Pool(2500)
		self.file = r_file
		self.ruleset = d_ruleset
	# Scan line
	# IN: line, dir(regex)
	# OUT: <<Prints>> Result
	def parse_line(self, line, regex):
		p = re.compile(regex[1])
		r_line = json.loads(line)
		data = base64.b64decode(r_line['data'])
		m = p.search(data)
		if m:
			start = m.span()[0] - 50
			if start < 0:
				start = 0
			end = m.span()[1] + 100
			if end > len(data):
				end = len(data)
			print "%s:%s - %s - %s" % (r_line['host'], r_line['port'], regex[0], repr(data[start:end]))
	# Start scanner
	# IN:
	# OUT:
	def start(self):
		if self.file.endswith(".gz"):
			file_lines = gzip.open(self.file, 'r')
		else:
			file_lines = open(self.file, 'r')
		counter = 0
		for line in file_lines:
                        for regex in self.ruleset:
                                self.pool.spawn(self.parse_line, line, regex )
                                counter += 1

		self.pool.join()

# Validates regular expression
# IN: r_regex
# OUT: boolean(result)
def regex_valid(r_regex):
	try:
		re.compile(r_regex)
		return True
	except re.error:
		return False	

# Scan using a user-provided regex
# IN: r_file, r_regex
# OUT: 
def single_scan(r_file, r_regex):
	if not regex_valid(r_regex):
		print " [x] Invalid Regex"
		return False
	ruleset = []
	ruleset.append([' ',r_regex])
	scan = ISD_Scanner(r_file, ruleset)
	scan.start()
# Scan using all rules or the name of a user-provided rule
# IN: r_file, r_name
# OUT:
def scan_full(r_file, r_name = None):
	d_rules = database()
	ruleset = []
	if r_name:
	        for rule in  d_rules.list_rules():
			if rule[0] == r_name:
				ruleset.append([rule[0],rule[1]])
	else:
		ruleset = d_rules.list_rules()
        scan = ISD_Scanner(r_file, ruleset)
        scan.start()

# Add rule to DB
# IN: r_name, r_regex
# OUT: 
def add_rule(r_name, r_regex):
	if regex_valid(r_regex):
        	d_rules = database()
		d_rules.submit_rule(r_name, r_regex)
# List rules
# IN:
# OUT: <<Print>> rules
def list_rule():
	d_rules = database()
	for rule in  d_rules.list_rules():
		print "%s => /%s/" % (rule[0], rule[1])

