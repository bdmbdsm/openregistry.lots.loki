from setuptools import setup, find_packages
import os

version = '0.3.4'

entry_points = {
    'openregistry.lots.core.plugins': [
        'lots.loki = openregistry.lots.loki.includeme:includeme'
    ],
    'openregistry.tests': [
        'lots.loki = openregistry.lots.loki.tests.main:suite'
    ],
    'lots.loki.migration': [
        'main = openregistry.lots.loki.migration:migrate'
    ]
}

requires = [
    'setuptools',
    'openprocurement.api',
    'openregistry.lots.core'
]

test_requires = requires + []

docs_requires = requires + [
    'sphinxcontrib-httpdomain',
]

setup(name='openregistry.lots.loki',
      version=version,
      description="",
      long_description=(
          open("README.rst").read() +
          "\n" +
          open(os.path.join("docs", "HISTORY.txt")).read()
      ),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Quintagroup, Ltd.',
      author_email='info@quintagroup.com',
      license='Apache License 2.0',
      url='https://github.com/openprocurement/openregistry.lots.loki',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['openregistry', 'openregistry.lots'],
      include_package_data=True,
      zip_safe=False,
      extras_require={'docs': docs_requires, 'test': test_requires},
      install_requires=requires,
      entry_points=entry_points,
      )
