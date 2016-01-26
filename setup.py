from distutils.core import setup
import os
import itertools
from setuptools import find_packages

setup(
    # Application name:
    name="Drone",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Paulius Klyvis",
    author_email="paul@foje.lt",

    # Packages
    packages=find_packages(),

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/grafke/Drone-workflow-controller",

    #
    # license="LICENSE.txt",
    description="Platform to schedule and monitor workflows.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "Flask",
        "setuptools",
        "boto3",
        "flask-cors"
    ],
    scripts=['drone/bin/drone_app.py'],
    data_files=[('/etc/drone/', ['drone/config/remote_jobs_config.json']),
                ('/etc/drone/', ['drone/config/aws_jobs_config.json.template']),
                ('/usr/local/bin/', ['drone/actions/remote_action_launcher.sh']),
                ('/var/www', ['drone-web/index.html']),
                ('/var/www/css', ['drone-web/css/drone.css', 'drone-web/css/foundation.css',
                                         'drone-web/css/jquery.dataTables.min.css']),
                ('/var/www/images/',
                 ['drone-web/images/sort_asc.png', 'drone-web/images/sort_both.png', 'drone-web/images/sort_desc.png']),
                ('/var/www/js/',
                 ['drone-web/js/drone-core.js', 'drone-web/js/drone-core.js', 'drone-web/js/jquery.dataTables.min.js',
                  'drone-web/js/jquery-1.11.3.min.js']),
                ('/var/www/js/foundation/',
                 ['drone-web/js/foundation/foundation.js', 'drone-web/js/foundation/foundation.dropdown.js'])]
)
