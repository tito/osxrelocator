from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='osxrelocator',
    version='1.0.1',
    description='Utility to relocate OSX libraries',
    long_description=long_description,
    url='https://github.com/tito/osxrelocator',
    author='Mathieu Virbel',
    author_email='mat@meltingrocks.com',
    license='LGPL2',
    packages=['osxrelocator'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    keywords='osx libraries relocation setuptools development',
    entry_points={
        'console_scripts': [
            'osxrelocator=osxrelocator:main',
        ],
    },
)
