import os
import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


APP_NAME = 'src'


def get_version():
    init_path = os.path.join(APP_NAME, '__init__.py')
    content = read_file(init_path)
    match = re.search(r"__version__ = '([^']+)'", content, re.M)
    version = match.group(1)
    return version


def read_requirements(filename):
    contents = read_file(filename).strip('\n')
    return contents.split('\n') if contents else []


def read_file(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path) as f:
        return f.read()


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            'tests',
            APP_NAME,
            '--pep8',
            '--flakes',
            '--cov', APP_NAME,
            '--cov-report', 'term-missing',
        ]
        self.test_suite = True

    def run_tests(self):
        # Importing here, `cause outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


install_requires = read_requirements('requirements.txt')
tests_require = read_requirements('requirements_dev.txt')

setup(
    name=APP_NAME,
    version=get_version(),
    author='Marcin Dziedzic',
    author_email='marcin.dziedzic@pragmaticcoders.com',
    description='Description of app or library',
    long_description=read_file('README.rst'),
    url='https://bitbucket.org/marcindziedzic/repo/src',
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
    ],
    packages=['src'],
    include_package_data=True,
    zip_safe=False,
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'app=app.main:main',
        ],
    },
)
