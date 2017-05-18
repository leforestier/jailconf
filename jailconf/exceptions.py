class ConfError(Exception):
    pass

class ConfTokenError(ConfError):
    pass

class ConfSyntaxError(ConfError):
    pass
    
class ConfSemanticError(ConfError):
    pass
