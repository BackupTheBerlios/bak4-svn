# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the GNU General Public License


__all__ = ['Parser', 'Scanner', 'ParsingError', 'ScanningError', 'processor']


from spark import GenericParser, GenericScanner
from mytoken import Token


class ParsingError (Exception):
    pass


class ScanningError (Exception):
    pass


class Parser (GenericParser):
    
    def __init__(self, start):
        GenericParser.__init__(self, start)
        
    def debug(self, *msg):
        for i in msg:
            print i,
        print
    
    def error(self, token):
        raise ParsingError, 'Error: unexpected token at or near "%s".' \
                % token.value


class Scanner (GenericScanner):
    
    def push(self, token_type, token_value=None):
        self.rv.append(Token(token_type, token_value))
    
    def tokenize(self, input):
        self.rv = []
        self.lineno = 1
        GenericScanner.tokenize(self, input)
        return self.rv
    
    def t_newline(self, s):
        r' \n+ '
        self.lineno += len(s)
    
    def t_ignore(self, s):
        r' \s+ '
        pass
    
    def t_ignore_comment(self, s):
        r' \# .* '
        pass
    
    def t_default(self, s):
        r' ( . )* '
        errlen = min(len(s), 10)
        raise ScanningError, 'Error at line %d, at or near "%s"' % \
                        (self.lineno, s[:errlen])


def processor(scanner_class, parser_class, debug=False):
    
    assert issubclass(scanner_class, Scanner)
    assert issubclass(parser_class, Parser)
    
    def process(string=None, filename=None, debug=debug):
        if string is None:
            if filename is not None:
                from os.path import expanduser
                filename = expanduser(filename)
                string = open(filename).read()
            else:
                raise ValueError, 'Nothing to parse.'
        
        tokens = scanner_class().tokenize(string)        
        rv = parser_class().parse(tokens)
        
        return rv
    
    return process
