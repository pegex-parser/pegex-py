from package.unittest import *

import pegex.grammar.pegex
import pegex.parser

class TestImport(TestCase):
    def test_parse_pegex(self):
        
        parser = pegex.parser.Parser(
            grammar='pegex.grammar.pegex',
            receiver='pegex.ast',
            debug=True
        )
        input_ = """\
a: <b>
b: /c/
"""
        ast = parser.parse(input)
        self.assertTrue(True, 'Parse probably worked')

if __name__ == '__main__':
    main()
