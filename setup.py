from setuptools import find_packages, setup

setup(
    name='TracSvn2GitChangesets', version='0.1',
    packages=find_packages(exclude=['*.tests*']),
    entry_points = {
        'trac.plugins': [
            'svn2gitchangesets = svn2gitchangesets.plugin',
        ],
    },
)