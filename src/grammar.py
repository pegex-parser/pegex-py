
import sys
import yaml
import pprint

def run():
    try:
        grammar = yaml.load(open(sys.argv[1]))
    except:
        raise # XXX

    data = pprint.pformat(grammar, indent=2)

    module = """\
\"\"\"
Pegex Grammar module for pegex
\"\"\"

class Grammar():
    def __init__(self):
        self.tree = {}
        self.tree.update(
        %(data)s
        )
""" % locals()

    print module

if __name__ == '__main__':
    run()
