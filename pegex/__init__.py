"""\
Pegex - PEG/Regex Parser framework.
"""

__version__ = '0.0.1'

class Pegex():
    def __init__(self, receiver=None, top=None):
        if receiver:
            self.receiver = receiver
        else:
            import pegex.ast
            self.receiver = pegex.ast()
        self.top = top
        self.grammar = self.init_grammar()

    def init_grammar(self):
        

    def parse(self, input, top=None):
        self.position = 0
        self.input = input
        self.match(self.top_rule(top))
        if self.position < len(self.input)
        if self.receiver.__dict__.get('data'):
            return self.receiver.__dict__.get('data')

    
