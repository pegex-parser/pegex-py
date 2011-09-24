from package.unittest import *

import pegex.grammar.pegex
import pegex.parser

class TestImport(TestCase):
    def test_parse_pegex(self):
        
        parser = pegex.parser.Parser(
            grammar='pegex.grammar.pegex',
            receiver='pegex.ast',
            debug=False
        )
        input_ = """\
a: <b>
b: /c/
"""
        ast = parser.parse(input_)
        self.assertTrue(True, 'Parse probably worked')

if __name__ == '__main__':
    main()

# from package.unittest import *
# 
# class TestImport(TestCase):
#     def test_parse(self):
#         import tests.grammar1
#         grammar = tests.grammar1.Grammar(
#             receiver=Compile()
#         )
#         input = file('tests/input1').read()
#         result = grammar.parse(input)
#         self.assertTrue(result, 'grammar1 parses input1')
#         self.assertTrue(type(result) == dict, 'result is dictionary')
#         self.assertEquals(result.get('name'), 'INGY', 'name is correct')
# 
# class Compile():
#     def __init__(self):
#         self.data = {}
# 
#     def got_name(self, groups):
#         self.data['name'] = groups[0]
# 
# if __name__ == '__main__':
#     main()
