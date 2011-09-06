from package.unittest import *

class TestImport(TestCase):
    def test_import(self):
        import pegex
        import pegex.grammar
        import pegex.grammar.pegex

        self.assertTrue(True, 'pegex modules imported cleanly')

if __name__ == '__main__':
    main()
