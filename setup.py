# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='dev-dir-sync',
      version='0.1',
      description="Fast cross platform dir watcher that syncs updates using rsync",

      author='Shlomi Atar',
      author_email='shlomi@smore.com',
      url='',
      packages=['dir_sync'],

      classifiers=[
          'Programming Language :: Python',
      ],

      platforms='Any',
      keywords=('monitor', 'directory', 'sync'),


      package_dir={'': '.', 'dir_sync': 'dir_sync'},
      install_requires=['watchdog >= 0.7.1'],

      # A console script for starting the server
      entry_points={
          'console_scripts': [
              'dir_sync = dir_sync:boot'
          ]
      }
)
