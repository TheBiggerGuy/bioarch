#!/usr/bin/env python3

from codecs import open  # To use a consistent encoding
from os import path, system
import re
import sys

# Always prefer setuptools over distutils
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand  # noqa: N812


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        import pytest  # import here, cause outside the eggs aren't loaded
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


if sys.argv[-1] == 'publish':
    system('python setup.py sdist upload')
    sys.exit()

with open('bioarc/__init__.py', 'r') as fd:
    contents = fd.read()
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        contents, re.MULTILINE).group(1)
    title = re.search(r'^__title__\s*=\s*[\'"]([^\'"]*)[\'"]',
                      contents, re.MULTILINE).group(1)
    author = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]',
                       contents, re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')
if not title:
    raise RuntimeError('Cannot find title information')
if not author:
    raise RuntimeError('Cannot find author information')

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=title,
    version=version,
    description='Python bioarchaeology',
    long_description=long_description,
    author=author,
    author_email='thebigguy.co.uk@gmail.com',
    url='https://github.com/TheBiggerGuy/pybioarch',
    packages=find_packages(exclude=['docs', 'tests']),
    package_data={'': ['LICENSE', 'README.md']},
    zip_safe=False,
    install_requires=[],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    keywords=[],
    license='MIT',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
