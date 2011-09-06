""""\
##
# name:      Pegex::AST
# abstract:  Pegex Abstract Syntax Tree Object Class
# author:    Ingy dot Net <ingy@cpan.org>
# license:   perl
# copyright: 2011
"""

from pegex.receiver import Receiver

class AST(Receiver):

    def __init__(self):
        self.data = None
        Receiver.__init__(self)

    def got(self, rule, definition):
        return dict(rule=definition)

    def final(self, match, top):
        if match is IGNORE:
            final = {top: {}}
        else:
            final = match
        self.data = final
        return final

