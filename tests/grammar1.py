"""
Generated Pegex test grammar
"""

import pegex.grammar

class Grammar(pegex.grammar.Grammar):
    def __init__(self, receiver=None):
        pegex.grammar.Grammar.__init__(self, receiver=receiver)
        self.grammar = {}
        self.grammar.update(
{ '_FIRST_RULE': 'greeting',
  'greeting': { '+all': [ {'+rule': 'nicety'},
                          {'+re': '\\s'},
                          {'+rule': 'name'},
                          {'+rule': 'punctuation', '<': '?'},
                          {'+re': '\\r?\\n'}]},
  'name': {'+re': '[A-Z]\\w*'},
  'nicety': {'+re': '(Hello|O HAI|Hey)'},
  'punctuation': {'+re': '[\\.,!]'}}
)
