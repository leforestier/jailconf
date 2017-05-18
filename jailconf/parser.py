from jailconf.exceptions import ConfSyntaxError
from jailconf.lexer import Lexer
from jailconf.structures import JailConf, JailBlock, Append

from ply import yacc

__all__ = ['loads']

class Parser(object):
    
    def p_conf(self, p):
        " conf : global_scope "
        p[0] = p[1]
        
    def p_global_scope_1(self, p):
        """ global_scope : global_scope statement 
            global_scope : global_scope jail_definition """
        p[0] = p[1]
        p[0].update((p[2],))
        
    def p_global_scope_empty(self, p):
        " global_scope : "
        p[0] = JailConf()
        
    def p_jail_block(self, p):
        " jail_definition : value OPEN_BRACE statement_list CLOSE_BRACE "
        p[0] = (p[1], JailBlock(p[3]))
        
    def p_statement_list(self, p):
        " statement_list : statement_list statement "
        p[0] = p[1] + (p[2],)
        
    def p_statement_list_empty(self, p):
        " statement_list : "
        p[0] = ()
        
    def p_statement(self, p):
        """ statement : affectation
            statement : declaration 
            statement : append """
        p[0] = p[1]
        
    def p_affectation(self, p):
        """ affectation : parameter EQUAL value SEMICOLON
            affectation : parameter EQUAL many_values SEMICOLON """
        p[0] = (p[1], p[3])
        
    def p_append(self, p):
        " append : parameter PLUS_EQUAL value SEMICOLON "
        p[0] = Append(p[1], p[3])
        
    def p_declaration(self, p):
        " declaration : parameter SEMICOLON "
        p[0] = (p[1], True)
        
    def p_parameter(self, p):
        " parameter : NAME "
        p[0] = p[1]
        
    def p_value(self, p):
        """ value : NAME
            value : SINGLE_QUOTED_STRING
            value : DOUBLE_QUOTED_STRING """
        p[0] = p[1]
        
    def p_many_values(self, p):
        " many_values : many_values COMMA value "
        p[0] = p[1]
        p[0].append(p[3])
        
    def p_many_values_only_two(self, p):
        " many_values : value COMMA value "
        p[0] = [p[1], p[3]]   
        
    def p_error(self, p):
        raise ConfSyntaxError(repr(p))
        
    def __init__(self, lexer = None):
        lexer = lexer or Lexer()
        self.tokens = lexer.tokens
        self._lexer = lexer
        self._parser = yacc.yacc(module=self, debug=False, write_tables=0)
        
    def parse(self, entry):
        return self._parser.parse(
            entry,
            lexer = self._lexer.lexer
        )

loads = Parser().parse

def load(path):
    with open(path) as fp:
        return loads(fp.read())

if __name__ == '__main__':
    import sys
    text = sys.stdin.read()
    print()
    print(loads(text).dumps())
