import os
from setuptools import setup

def read(fname):
    """Get the contents of the named file as a string."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pyrecommend',
    version='0.1',
    author='Dan Passaro',
    author_email='danpassaro@gmail.com',
    description=('A simple collaborative filtering algorithm for Python.'),
    license='BSD',
    packages=['pyrecommend'],
    long_description=read('README.md'),
)
