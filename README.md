SVN to Git changeset trac tools
====================

Brett Profitt 2011
GPL 2

Bits of the migration tools based upon https://github.com/poseidix/TRAC-SVN-to-GIT-migration

About
-----

This is useful only if you are migrating a trac installation from SVN to Git on GitHub.

You probably also want to install these plugins:
	* https://github.com/davglass/github-trac
	* http://trac-hacks.org/wiki/GitPlugin

Configuration
-------------

 1. Backup everything in SVN and trac.
 2. Import your SVN repo to git. (Google can help.)
 3. Create a map of your SVN comits to their git refs. (See tools/svn2git_refs.sh)
 4. Rewrite the trac database. (See tools/rewrite_database.py)
 5. Install and configure trac plugins. (easy_install. Google can help.)

Trac configuration
------------------

Add the following to your trac.ini file:
	[svn2gitchangesets]
	changesets_url = https://github.com/<github username>/<repo name>/commit/%s
	pickled_map = /path/from/step/4/to/svn2git_commits.pkl
	
	[components]
	svn2gitchangesets.* = enabled

