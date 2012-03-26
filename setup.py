from setuptools import setup, find_packages
import os

version = '0.0.14'

setup(name='bit.core',
      version=version,
      description="Core interfaces for bit framework",
      long_description=open("bit/core/README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ryan Northey',
      author_email='ryan@3ca.org.uk',
      url='http://github.com/bitf/bit.core',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bit'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.interface',
          'zope.component',
          'zope.configuration',
          'zope.dottedname',
          'twisted',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
