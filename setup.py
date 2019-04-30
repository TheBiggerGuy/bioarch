#!/usr/bin/env python3

from os import getenv, path
import re
import sys

# Always prefer setuptools over distutils
from setuptools import find_packages, setup
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand  # noqa: N812


class MetatDataFetcher(object):
    """docstring for MetatDataFetcher"""
    def __init__(self, module_name):
        pwd = path.abspath(path.dirname(__file__))

        with open(path.join(pwd, module_name, '__init__.py'), mode='r', encoding='utf-8') as fd:
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
        self.version = version
        self.title = title
        self.author = author

        # Get the long description from the README file
        with open(path.join(pwd, 'README.md'), mode='r', encoding='utf-8') as f:
            long_description = f.read()
        if not long_description:
            raise RuntimeError('Cannot find long_description information')
        self.long_description = long_description


meta_data = MetatDataFetcher('bioarch')


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        circleci_tag = getenv('CIRCLE_TAG')

        if circleci_tag is None:
            sys.exit(f'Faied to find "CIRCLE_TAG" env')

        if circleci_tag != ('v' + meta_data.version):
            info = f'CircleCI Git tag "{circleci_tag}" does not match the version of this app "{meta_data.version}"'
            sys.exit(info)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''  # pylint: disable=W0201

    def run_tests(self):
        import shlex
        import pytest  # import here, cause outside the eggs aren't loaded
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name=meta_data.title,
    version=meta_data.version,
    description='Python bioarchaeology',
    long_description=meta_data.long_description,
    long_description_content_type='text/markdown',
    author=meta_data.author,
    author_email='thebigguy.co.uk@gmail.com',
    url='https://github.com/TheBiggerGuy/bioarch',
    packages=find_packages(exclude=['docs', 'tests']),
    package_data={'': ['LICENSE', 'README.md']},
    zip_safe=False,
    install_requires=[],
    tests_require=['pytest'],
    cmdclass={
        'test': PyTest,
        'verify': VerifyVersionCommand,
    },
    keywords=[],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3 :: Only",
        'Programming Language :: Python :: Implementation :: CPython',
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3',
)
