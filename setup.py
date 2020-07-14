from setuptools import setup
import sys

with open('README.rst') as fd:
    long_description = fd.read()

setup(
    name='jailconf',
    version='0.2.2',
    packages=['jailconf'],
    install_requires = ['ply>=3.9'],
    python_requires='>=3.0',
    author = 'Benjamin Le Forestier',
    author_email = 'benjamin@leforestier.org',
    url = 'https://github.com/leforestier/jailconf',
    keywords = ["jail.conf", "parse", "edit", "configuration", "freebsd", "jail"],
    description = "Parse and edit your FreeBSD jail.conf file",
    long_description = long_description,
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Systems Administration',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
