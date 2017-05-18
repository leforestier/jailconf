from jailconf.exceptions import ConfSemanticError
from jailconf.lexer import Lexer

from collections import OrderedDict
import os
import re
from tempfile import mkstemp

class Append(object):
    def __init__(self, param, value):
        self.param = param
        self.value = value

class Conf(OrderedDict):

    valid_param_rgx = re.compile('^%s$' % Lexer.t_NAME.__doc__)
    valid_value_rgx = re.compile('^(%s)$' % '|'.join((
        Lexer.t_NAME.__doc__,
        Lexer.t_SINGLE_QUOTED_STRING.__doc__,
        Lexer.t_DOUBLE_QUOTED_STRING.__doc__
    )))
    
    @classmethod
    def validate_param(cls, param):
        if cls.valid_param_rgx.match(param):
            return param
        else:
            raise ValueError("Invalid parameter %s" % repr(param))
            
    @classmethod
    def validate_value(cls, value):
        if cls.valid_value_rgx.match(value):
            return value
        else:
            raise ValueError("Invalid value %s" % repr(value))
            
    @classmethod
    def validate_key_value(cls, key, value):
        if isinstance(value, JailBlock):
            cls.validate_value(key)
        else:
            cls.validate_param(key)
            if isinstance(value, str):
                cls.validate_value(value)
            elif isinstance(value, list):
                if len(value) < 2:
                    raise ValueError("Lists of values should have at least 2 elements.")
                for v in value:
                    cls.validate_value(v)
            elif value is not True:
                raise ValueError(
                    "Invalid type for value %s. Should be of type str, list, JailBlock, or should be the value True."
                    % repr(value)
                )
        return key, value
         
    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("Expected at most 1 argument, got 2")
        if args:
            if hasattr(args[0], 'keys'):
                lst = [(k,args[0][k]) for k in args[0].keys()]
            else:
                lst = args[0]
        else:
            lst = []
        if kwargs:
            lst.extend(kwargs.items())
        for item in lst:
            if isinstance(item, Append):
                if item.param in self:
                    if isinstance(self[item.param], str):
                        super(Conf, self).__setitem__(item.param, [self[item.param], item.value])
                    elif isinstance(self[item.param], list):
                        self[item.param].append(item.value)
                    else:
                        raise ConfSemanticError(
                            "Trying to append to parameter %s but it has type %s" % (
                                item.param, type(self[item.param])
                            )
                        )
                else:
                    raise ConfSemanticError(
                        "Trying to append to undefined parameter %s" % item.param
                    )
            else:
                key, value = item
                self[key] = value

        
    def __setitem__(self, k, v):
        self.__class__.validate_key_value(k, v)
        super(Conf, self).__setitem__(k, v)
    
    def __init__(self, *args, **kwargs):
        super(Conf, self).__init__()
        self.update(*args, **kwargs)
        
    def strgen(self, indentation = '\t', current_indent = 0):
        for key, value in self.items():
            yield current_indent * indentation
            yield key
            if isinstance(value, JailBlock):
                yield ' {\n'
                yield from value.strgen(indentation, current_indent + 1)
                yield '}\n'
            elif value is True:
                yield ';\n'
            elif isinstance(value, list):
                yield ' = %s;\n' % (', '.join(value))
            else:
                yield ' = %s;\n' % value
    
    def dumps(self, indentation = '\t', current_indent = 0):
        return ''.join(self.strgen(indentation, current_indent))
        
    def write(self, path, indentation = '\t'):
        handle, temp_path = mkstemp(prefix = path)
        os.write(handle, self.dumps(indentation = indentation).encode('utf-8'))
        os.close(handle)
        os.rename(temp_path, path)
    
class JailConf(Conf):
    def jails(self):
        for key, value in self.items():
            if isinstance(value, JailBlock):
                yield (key, value)
        
class JailBlock(Conf):
    @classmethod
    def validate_key_value(cls, k, v):
        if isinstance(v, JailBlock):
            raise ValueError("Jail block not allowed in this context.")
        return super(JailBlock, cls).validate_key_value(k, v)
