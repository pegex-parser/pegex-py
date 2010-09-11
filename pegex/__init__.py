"""\
Pegex - PEG/Regex Parser framework.
"""

__version__ = '0.0.1'

class Pegex():
    def __init__(self, grammar):
        self.grammar = grammar

    def pegex(grammar_text):
        import pegex.grammar
        return Pegex(pegex.grammar.Grammar(grammar_text=grammar_text))

    def compile(self):
        self.grammar.compile()
        return self

    def parse(self, input, start_rule=None):
        return self.grammar.parse(input, start_rule)
