import unittest
from jailconf import loads, JailConf, JailBlock

class TestJailConf(unittest.TestCase):

    def setUp(self):
        # Example configuration inspired by
        # https://www.freebsd.org/cgi/man.cgi?query=jail.conf&sektion=5&n=1
        self.jail_conf_in = """\
# Typical static defaults:
# Use the rc scripts to start and stop jails.  Mount jail's /dev.
exec.start	= "/bin/sh /etc/rc";
exec.stop = "/bin/sh /etc/rc.shutdown";
exec.clean;
mount.devfs;

# Dynamic wildcard	parameter:
# Base the	path off the jail name.
path = "/var/jail/$name";

# A typical jail.
foo {
    host.hostname = "example.com";
    ip4.addr = 10.1.1.1, 10.1.1.2, 10.1.1.3;
    ip4.addr += 10.1.1.4;
}

# This jail overrides the defaults	defined	above.
bar {
    exec.start = '';
    exec.stop = '';
    path = /;
    mount.nodevfs;
    persist;	     //	Required because there are no processes
}"""

        self.jail_conf_out = """\
exec.start = "/bin/sh /etc/rc";
exec.stop = "/bin/sh /etc/rc.shutdown";
exec.clean;
mount.devfs;
path = "/var/jail/$name";
foo {
    host.hostname = "example.com";
    ip4.addr = 10.1.1.1, 10.1.1.2, 10.1.1.3, 10.1.1.4;
}
bar {
    exec.start = '';
    exec.stop = '';
    path = /;
    mount.nodevfs;
    persist;
}
"""
 
    def test1(self):
        self.assertEqual(
            loads(self.jail_conf_in).dumps(indentation = '    '),
            self.jail_conf_out
        )
    
    def test2(self):
        jail_conf = loads(self.jail_conf_in)
        jail_conf['myjail'] = JailBlock([('ip4.addr', '192.168.1.10')])
        del jail_conf['bar']['path']
        jail_conf['path'] = '"/var/jails/$name"'
        jail_conf['foo']['ip4.addr'] = ['192.168.1.11', '192.168.1.12']
        expected_output = """\
exec.start = "/bin/sh /etc/rc";
exec.stop = "/bin/sh /etc/rc.shutdown";
exec.clean;
mount.devfs;
path = "/var/jails/$name";
foo {
    host.hostname = "example.com";
    ip4.addr = 192.168.1.11, 192.168.1.12;
}
bar {
    exec.start = '';
    exec.stop = '';
    mount.nodevfs;
    persist;
}
myjail {
    ip4.addr = 192.168.1.10;
}
"""
        self.assertEqual(jail_conf.dumps(indentation = '    '), expected_output)
        
