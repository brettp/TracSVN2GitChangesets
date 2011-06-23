#!/usr/bin/env python

import pickle

commits = {}
for line in file('svn2git_changesets.tsv'):
	line = line.split()
	if len(line) is 2:
		commits[line[0]] = line[1]

output = open('svn2git_changesets.pkl', 'wb')
pickle.dump(commits, output)

