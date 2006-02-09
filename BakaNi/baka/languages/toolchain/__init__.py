# encoding: utf-8

# copyright (c) domenico carbotta <domenico.carbotta@gmail.com>, 2005
# code released under the GNU General Public License


__all__ = ['Parser', 'Scanner', 'ParsingError', 'ScanningError', 'processor']


from spark import GenericParser, GenericScanner
from mytoken import Token
from os.path import expanduser


class ParsingError (Exception):
    pass


class ScanningError (Exception):
    pass


class Parser (GenericParser, object):
    
    def __init__(self, start):
        GenericParser.__init__(self, start)
    
    def debug(self, *msg):
        for i in msg: #-#
            print i, #-#
        print #-#
        pass
    
    def error(self, token):
        raise ParsingError, 'Error: unexpected token at or near "%s".' \
                % token.value


class Scanner (GenericScanner, object):
    
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


def processor(scanner_factory, parser_factory, debug=False):
    
    def process(what, is_filename=False, debug=debug):
        if is_filename:
            string = open(expanduser(what)).read()
        else:
            string = what
        
        tokens = scanner_factory().tokenize(string)
        
        if debug:
            print 'tokens = ['
            print '\t', ',\n\t'.join(map(repr, tokens))
            print ']'
            print
        
        rv = parser_factory().parse(tokens)
        
        if debug:
            print 'result =', rv
        
        return rv
    
    return process
