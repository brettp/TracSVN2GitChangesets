#!/usr/bin/python
"""
convertTracTickets.py

Converts a trac.db changeset references to from [1234] and r1234 to [svn:1234].

Brett Profitt
GPL 2
"""

import sys
import sqlite3
import os
import re

if len(sys.argv) < 2:
	print "Must specify the database."
	print "Usage: %s trac.db" % sys.argv[0]
	sys.exit()

db_file = sys.argv[1]

if not os.path.isfile(db_file):
	print "Could not open file `%s`." % db_file
	sys.exit()	

con = sqlite3.connect(db_file)
con.row_factory = sqlite3.Row

# quick test to see if this is a real db. Probably a better way.

try:
	con.execute("SELECT * FROM ticket LIMIT 1")
except:
	print "Could not open db."
	sys.exit()

def convertText(value):
	if value is None or value == "":
		return ""

	patterns = [
		r'\[([0-9]+)\]',
		r'r([0-9]+)\s'
	]
	
	replace = r'[svn:\1]'
	
	for pattern in patterns:
		value = re.sub(pattern, replace, value)
		
	return value

print "Rewriting database..."

# change tickets
tickets = con.execute('SELECT * FROM ticket')

for ticket in tickets:
	new_description = convertText(ticket['description'])
	
	if new_description != ticket['description']:
		print "Rewriting description for ticket #%s..." % (ticket['id'])
		#$query = "UPDATE ticket SET description='$description_new' WHERE id = " . $row['id'];
		con.cursor().execute("UPDATE ticket SET description=? WHERE id=?", (new_description, ticket['id']))

con.commit()

# change ticket changes (including comments and commit commits)
changes = con.execute('SELECT * FROM ticket_change')

for change in changes:
	new_oldvalue = convertText(change['oldvalue'])
	new_newvalue = convertText(change['newvalue'])
	
	if new_oldvalue != change['oldvalue'] or new_newvalue != change['newvalue']:
		print "Rewriting ticket_change for #%s @ %s..." % (change['ticket'], change['time'])
		
		con.cursor().execute("UPDATE ticket_change SET oldvalue=?, newvalue=? WHERE ticket=? AND time=? AND author=? and field=?", 
			(new_oldvalue, new_newvalue, change['ticket'], change['time'], change['author'], change['field']))
			
con.commit()

print "Database rewrite complete."