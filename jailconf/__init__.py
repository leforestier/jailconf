"""
Parse and edit your FreeBSD jail.conf file with python.

Examples:

import jailconf
conf = jailconf.load('/etc/jail.conf')

conf['path'] = '"/var/jail/$name"'
conf['mount.devfs'] = True
conf['myjail'] = jailconf.JailBlock()
conf['myjail']['ip4.addr'] = ['10.0.0.1', '10.0.0.2']
conf['myjail']['host.hostname'] = 'example.com'

conf.write('/etc/jail.conf') # overwrite configuration file

A bit more documentation in the README.rst.
    https://github.com/leforestier/jailconf/blob/master/README.rst
"""

from jailconf.parser import loads, load
from jailconf.structures import JailConf, JailBlock

__author__ = "Benjamin Le Forestier (benjamin@leforestier.org)"
__version__ = '0.2.2'
