from setuptools import setup, find_packages
import os

version = '2.0'

long_description = (
    open('README.md').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='py-scopes',
      version=version,
      description="combined triple and event storage for the cco application platform",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='cyberconcepts.org team',
      author_email='team@cyberconcepts.org',
      url='http://www.cyberconcepts.org',
      license='MIT',
      packages=find_packages(),
      #package_dir = {'': 'src'},
      #namespace_packages=['cco'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'transaction',
          'psycopg2-binary',
          'SQLAlchemy',
          'zope.sqlalchemy',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
