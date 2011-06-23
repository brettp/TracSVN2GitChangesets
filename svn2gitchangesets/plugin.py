# -*- coding: utf-8 -*-
"""
svn2gitchangesets

Link [svn:1234] revisions to their git counterparts on github

Requires the DB to be migrating using the rewrite_database.py script.
Requires a map to be created using the svn2git_refs.py script.

Brett Profitt
"""

import pickle
import re

from trac.core import *
from trac.config import Option, IntOption, ListOption, BoolOption
from trac.wiki.api import IWikiSyntaxProvider

from genshi.builder import tag

class Svn2GitChangesets(Component):
	implements(IWikiSyntaxProvider)
	
	changesets_url = Option('svn2gitchangesets', 'changesets_url', doc="""The URL for the github changesets. %s is replaced with the changeset""")
	map_file = Option('svn2gitchangesets', 'map_file', doc="""The full path of the pickled SVN commit to github commit map file.""")

	pickled_map = open(map_file, 'rb')
	svn2git_map = pickle.load(map_file)
	
	# IWikiSyntaxProvider methods
	def get_wiki_syntax(self):
		yield (r'\[svn:(?P<revision>[0-9]+)\]', self._format_regex_link)

	def get_link_resolvers(self):
		''' 
		no link resolvers for this
		'''
		return []

	def _format_regex_link(self, formatter, match, fullmatch):
		rev = fullmatch.group('revision')
		#not sure why this doesn't work sometimes.
		#gh_rev = svn2git_map.get(rev)
		
		if rev in self.svn2git_map:
			gh_rev = self.svn2git_map[rev]
			return tag.a(match,
				href=self.changesets_url % (gh_rev),
				class_="changeset",
				title="SVN Changeset %s (Git changset %s)" % (rev, gh_rev))
		else:
			return tag.a(match,
				class_="missing changeset",
				title="Missing Changeset")
