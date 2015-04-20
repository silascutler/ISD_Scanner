#!/usr/bin/env python
#######################################################################
# Internet Scan Data Searcher                                         #
#######################################################################
# Copyright (C) 2015 Silas Cutler   <Silas.Cutler@Gmail.com>          #
#######################################################################
# This file is subject to the terms and conditions of the BSD License.#
#######################################################################

import os
import sqlite3

class database(object):
	# Init database
	# IN: 
	# OUT: 
	def __init__(self):
	        bool_new_db = self.db_pre_check()
	        try:
	                self.db_scan = sqlite3.connect('./db/scan.db')
	        except Exception, e:
	                print e
	                print "Failed to connect to db"
	                sys.exit(1)
	        if (bool_new_db):
	                self.db_initialize()

	# Create Table for rules / regexs
	# IN:
	# OUT: 
	def db_initialize(self):
	        self.db_scan.execute('''
	                        CREATE TABLE rules (
	                        name varchar(255) PRIMARY KEY NOT NULL,
	                        regex varchar(255) NOT NULL
	                	)''')
	# Validate DB file exists and create db file
	# IN:
	# OUT: 
	def db_pre_check(self):
	        if (os.path.isdir("./db") == False):
	                os.mkdir("./db")
	
	        try:
	                with open( './db/scan.db') as handle_db_check:
	                        return False
	        except IOError:
	                print " [+] Creating New Database"
	                return True
	# Insert rule into DB
	# IN: r_name, r_regex
	# OUT:
	def submit_rule(self, r_name, r_regex):
	        db_handle = self.db_scan.cursor()

	        sql_insert = "INSERT INTO rules VALUES (?, ?)"
	        try:
	                db_handle.execute(sql_insert, (r_name, r_regex))
	                self.db_scan.commit()
			print " [+] Inserted rule %s into db" % (r_name)
	        except Exception, e:
	                print e
	                print "Failed to submit to DB"
	# List rules in DB
	# IN:
	# OUT: dir(rules)
	def list_rules(self):
		db_cursor = self.db_scan.cursor()
		db_cursor.execute("SELECT name, regex FROM rules", ([]))
		return db_cursor.fetchall()
		
