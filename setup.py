from setuptools import setup, find_packages
import sys, os

version = '0.5'

setup(
    name='ckanext-harvest-tn',
    version=version,
    description="CKAN StatWeb harvesters for Trento",
    long_description="""\
    """,
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Emanuele Tajariol',
    author_email='etj@geo-solutions.it',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.harvest_tn'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
       # -*- Extra requirements: -*-
    ],
    entry_points=
    """
        [ckan.plugins]
        statwebpro_harvester=ckanext.harvest_tn.harvesters.statwebpro:StatWebProHarvester
        statwebsubpro_harvester=ckanext.harvest_tn.harvesters.statwebsubpro:StatWebSubProHarvester
    """,
)
