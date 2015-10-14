from distutils.core import setup
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
        "flask",
    ],
)