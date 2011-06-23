#!/bin/sh
#
# Originally from https://github.com/poseidix/TRAC-SVN-to-GIT-migration
# 
# This script creates a 'lookup table', matching SVN revision IDs with GIT revision IDs
# Run it inside a GIT repository that is imported from SVN with "git svn".
#
# Usage:
#       createLookupTable > lookupTable.txt

if [ $# -lt 1 ]; then
	echo "You must specify the repo directory."
	exit 1
fi

git_path=$1

if [ ! -d $git_path ]; then
	echo "You must specify the repo directory."
	exit 1
fi

tools_dir=`pwd`

# have to be in the git repo dir. --get-dir and --get-tree aren't reliable enough.
cd $git_path

# Creates a lookup table between SVN IDs and Git IDs
git rev-list --grep='git-svn-id' --all --pretty=medium > ${tools_dir}/revlist.txt;

cd ${tools_dir}

# Now extract the git hash and the svn ID. Then we join lines pair-wise and we have our table
cat ${tools_dir}/revlist.txt | grep git-svn-id | sed -e 's/git-svn-id: [a-z0-9 \#A-Z_\/:\.-]\{1,\}@\([0-9]\{1,4\}\) .\{1,\}/\1/' > ${tools_dir}/svn.txt;
cat ${tools_dir}/revlist.txt | grep ^commit > ${tools_dir}/git.txt;

# Join them and write the lookup table to a tsv file
paste ${tools_dir}/svn.txt ${tools_dir}/git.txt | sed -e 's/commit //' | sed -e 's/ //g' | sort -n > ${tools_dir}/svn2git_changesets.tsv

# Pickle the results
${tools_dir}/pickle_file.py

if [ $? -eq 0 ]; then
	echo "Pickled changesets in ${tools_dir}/svn2git_changesets.pkl"
	echo "Set the map_file option to this file in trac.ini"
fi

# Clean up
rm ${tools_dir}/svn.txt ${tools_dir}/git.txt ${tools_dir}/revlist.txt ${tools_dir}/svn2git_changesets.tsv
