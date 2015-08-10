# coding: utf-8
"""Script to upload to PyPI and tag in git."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import glob
import os.path
import runpy
import shutil
import subprocess
import sys


PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))


def path_to(*parts):
    """Get an absolute path to a file/folder in the project."""
    return os.path.join(PROJECT_DIR, *parts)


def clean_build_dirs():
    """Remove old build artifacts."""
    shutil.rmtree(path_to('build'))
    shutil.rmtree(path_to('dist'))


def build_package():
    """Build a source and binary wheel package."""
    subprocess.check_call([sys.executable, path_to('setup.py'),
                           'sdist', 'bdist_wheel'])


def upload_with_twine():
    """Upload to pypi.python.org using twine."""
    files = glob.glob(path_to('dist', '*'))
    subprocess.check_call([sys.executable, '-m', 'twine', 'upload'] + files)


def tag_git_commit_with_version():
    """Tag the latest git commit with the current package version."""
    current_version = subprocess.check_output([
        sys.executable, path_to('setup.py'), '-V']).strip()
    tag_str = 'v{}'.format(current_version)
    print('Tagging', tag_str, 'in git')
    subprocess.check_call(['git', '-C', PROJECT_DIR, 'tag', tag_str])


if __name__ == '__main__':
    clean_build_dirs()
    build_package()
    upload_with_twine()
    tag_git_commit_with_version()
