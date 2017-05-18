Parse and edit your FreeBSD jail.conf file with python.

Installation
~~~~~~~~~~~~

To install jailconf, simply:

.. code-block:: console

    pip3 install jailconf
    
jailconf requires Python 3.

Examples
~~~~~~~~

.. code:: python

    import jailconf
    
Load the configuration from a path

.. code:: python
   
    conf = jailconf.load('/etc/jail.conf')
    
Load the configuration from a string 
    
.. code:: python   
    
    conf = jailconf.loads(open('/etc/jail.conf').read())
    
Create an empty configuration

.. code:: python
    
    conf = jailconf.JailConf()
    
The configuration is represented as a dictionnary (actually a subclass of OrderedDict).
    
Let's modify some settings.

The quoted strings in the configuration should be passed with the quotes.
For example, to obtain the setting:

.. code:: sh
    
    path = "/var/jail/$name";

you write:

.. code:: python
    
    conf['path'] = '"/var/jail/$name"'
    
The string should be exactly what you want to appear on the right side of the
parameter name in the configuration file.
If you want the value of a parameter to be a quoted string, you pass
a string containing a quoted string.
This allows you to specify what kind of quotes you want to see in the output configuration 
file (single quotes, double quotes, or no quote at all).

.. code:: python
    
    conf['exec.start'] = '"/bin/sh /etc/rc"'
    conf['exec.stop'] = '"/bin/sh /etc/rc.shutdown"'
    
Boolean parameters. To obtain:

.. code:: sh

    exec.clean;
    mount.devfs;

you write:

.. code:: python
    
    conf['exec.clean'] = True
    conf['mount.devfs'] = True
    
Add a jail:

.. code:: python
    
    conf['myjail'] = jailconf.JailBlock([
        ('host.hostname', '"example.com"'),
        ('ip4.addr', ['10.1.1.1', '10.1.1.2', '10.1.1.3'])   
    ])
    
Modify a jail

.. code:: python
    
    conf['myjail']['ip4.addr'] = '192.168.1.2' # this will be rendered as the line: ip4.addr = 192.168.1.2
    
    # To set multiple ips, use a list:
    
    conf['myjail']['ip4.addr'] = ['192.168.1.2', '192.168.1.3']
    
Delete a jail

.. code:: python
    
    del conf['uselessjail']
    
Iterate over jails

.. code:: python
    
    for name, jail_block in conf.jails():
        jail_block['host.hostname'] = '"%s"' % name
        
Output the configuration as a string

.. code:: python
    
    >>> print(conf.dumps())

.. code::

    path = "/var/jail/$name";
    exec.start = "/bin/sh /etc/rc";
    exec.stop = "/bin/sh /etc/rc.shutdown";
    exec.clean;
    mount.devfs;
    myjail {
	    host.hostname = "myjail";
	    ip4.addr = 192.168.1.2, 192.168.1.3;
    }
    
Write the configuration to a file

.. code:: python
    
    conf.write('/etc/jail.conf')


GitHub repo: https://github.com/leforestier/jailconf
