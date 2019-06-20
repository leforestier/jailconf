from jailconf.exceptions import ConfTokenError

from ply import lex
import re


class Lexer(object):

    tokens = (
        'OPEN_BRACE',
        'CLOSE_BRACE',
        'EQUAL',
        'COMMA',
        'PLUS_EQUAL',
        'SEMICOLON',
        'NAME',
        'DOUBLE_QUOTED_STRING',
        'SINGLE_QUOTED_STRING'
    )

    t_OPEN_BRACE = '{'
    t_CLOSE_BRACE = '}'
    t_EQUAL = '='
    t_COMMA = ','
    t_PLUS_EQUAL = r'\+='
    t_SEMICOLON = ';'

    def t_ignore_NEW_LINE(self, token):
        r'\n'

    def t_ignore_C_STYLE_COMMENT(self, token):
        r'/\*((?!\*/).|\n)*\*/'

    def t_ignore_CPP_STYLE_COMMENT(self, token):
        r'//.*'

    def t_ignore_SHELL_STYLE_COMMENT(self, token):
        r'\#.*'

    def t_NAME(self, token):
        r'\$?[-a-zA-Z0-9._/*:]+'
        return token

    def t_DOUBLE_QUOTED_STRING(self, token):
        r'"(\\\\|\\"|[^"\\])*"'
        return token

    def t_SINGLE_QUOTED_STRING(self, token):
        r"'(\\\\|\\'|[^'\\])*'"
        return token

    t_ignore_space = r'[ \t]+'

    def t_error(self, token):
        raise ConfTokenError(
            "Illegal character '%s', line %s" % (
                token.value[0],
                token.lineno
            )
        )

    def __init__(self):
        self.lexer = lex.lex(object = self, debug = 0,reflags = re.MULTILINE)

if __name__ == '__main__':
    import sys
    lexer = Lexer().lexer
    lexer.input(sys.stdin.read())
    print()
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
