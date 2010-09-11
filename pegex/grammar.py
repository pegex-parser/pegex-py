"""\
pegex.grammar - Runtime base class for parsing grammars
"""

import re

class Grammar():
    def __init__(self, grammar_text=None, receiver=None, debug=False):
        self.grammar = None
        self.grammar_text = grammar_text
        self.grammar_tree = None
        # self.receiver = 'require Pegex::AST; Pegex::AST->new()';
        self.receiver = receiver
        self.debug = debug
        self.indent = 0

    def parse(self, input, start_rule=None):
        self.input = input
        self.position = 0
        self.match_groups = []

        if not self.grammar:
            self.compile()

        # XXX if receiver is a class, create an instance...
#         if type(self.receiver) == ???:
#             self.receiver = self.receiver()

        if not start_rule:
            if 'TOP' in self.grammar:
                start_rule = 'TOP'
            else:
                start_rule = self.grammar['_FIRST_RULE']

        self.action("__begin__")
        self.match(start_rule)
        if self.position < len(self.input):
            self.throw_error("Parse document failed for some reason")
        self.action("__end__")

        if getattr(self.receiver, 'data', None):
            return self.receiver.data
        else:
            return True

    def compile(self):
        grammar_tree = self.grammar_tree
        if not grammar_tree:
            grammar_text = self.grammar_text
            if not grammar_text:
                raise Error("%s object has no grammar" % type(self))
            import pegex.compiler
            grammar_tree = (
                pegex.compiler.Compiler()
                    .compile(grammar_text)
                    .combinate()
                    .grammar
            )
        self.grammar = grammar_tree
        return self

    def match(self, rule):
        not_ = False

        state = None
        if type(rule) == str and re.match(r'^\w+$', rule):
            if not self.grammar.get(rule):
                raise Error("\n\n*** No grammar support for 'rule'\n\n")
            state = rule
            rule = self.grammar[rule]

        times = rule.get('<') or '1'
        if rule.has_key('+not'):
            rule = rule['+not']
            kind = 'rule'
            not_ = True
        elif rule.has_key('+rule'):
            rule = rule['+rule']
            kind = 'rule'
        elif rule.has_key('+re'):
            rule = rule['+re']
            kind = 'regexp'
        elif rule.has_key('+all'):
            rule = rule['+all']
            kind = 'all'
        elif rule.has_key('+any'):
            rule = rule['+any']
            kind = 'any'
        elif rule.has_key('+error'):
            error = rule['+error']
            self.throw_error(error)
        else:
            raise Error("no support for rule")

        if state and not not_:
            self.callback("try_%s" % state)

            if self.debug:
                print ' ' * self.indent,
                self.indent += 1
                print "try_%s" % state

            self.action("__try__", state, kind)

        position = self.position
        count = 0
        method = 'match' if kind == 'rule' else ("match_%s" % kind)
        method_func = getattr(self, method)
        while method_func(rule):
            if not not_:
                position = self.position
            count += 1
            if times in '1?':
                break
        if count and times in '+*':
            self.position = position
        result = bool(count) or (times in '?*') ^ not_
        if result:
            self.position = position

        if state and not not_:
            if result:
                self.action("__got__", state, method)
            else:
                self.action("__not__", state, method)
            if result:
                self.callback("got_%s" % state)
            else:
                self.callback("not_%s" % state)
            self.callback("end_state")

            if self.debug:
                self.indent -= 1
                print ' ' * self.indent,
                if result:
                    print "got_%s" % state
                else:
                    print "not_%s" % state
        return result

    def match_all(self, list):
        for elem in list:
            if not self.match(elem):
                return False
        return True

    def match_any(self, list):
        for elem in list:
            if self.match(elem):
                return True
        return False

    def match_regexp(self, regexp):
        m = re.match(regexp, self.input[self.position:])
        if m:
            if m.groups():
                self.match_groups = m.groups()
            self.position += m.end()
            return True
        else:
            return False
    
    # XXX not entirely certain about calling method from str
    def action(self, method, state=None, kind=None):
        func = getattr(self.receiver, method, None)
        if func:
            func(self, self.match_groups)

    def callback(self, method):
        func = getattr(self.receiver, method, None)
        if func:
            func(self.match_groups)

    def throw_error(self, msg):
        line = self.input[0:self.position].count("\n") + 1
        context = self.input[self.position:self.position + 50]
        context = context.replace("\n", "\\n")
        position = str(self.position)
        formatted = """\
Error parsing Pegex document:
  msg: %(msg)s
  line: %(line)s
  context: "%(context)"
  position: %(position)s
""" % locals()
