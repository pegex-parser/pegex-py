from package.unittest import *

class TestImport(TestCase):
    def test_parse(self):
        import tests.grammar1
        grammar = tests.grammar1.Grammar(
            receiver=Compile()
        )
        input = file('tests/input1').read()
        result = grammar.parse(input)
        self.assertTrue(result, 'grammar1 parses input1')

class Compile():
    pass

if __name__ == '__main__':
    main()
