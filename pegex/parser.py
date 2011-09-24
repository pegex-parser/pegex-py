""""\
name:      Pegex::Parser
abstract:  Pegex Parser Runtime
author:    Ingy dot Net <ingy@cpan.org>
license:   perl
copyright: 2011
see:
- Pegex::Grammar
"""

class ParseException(BaseException):
    pass

#from __future__ import absolute_import

import re, os, sys

input_ = __import__('pegex.input', {}, {}, ['Input'])
Input = input_.Input

class Parser():

    def __init__(self, grammar=None, receiver='pegex.ast', debug=False):
        self.indent = 0
        self.grammar = grammar
        self.receiver = receiver
        self.throw_on_error = True
        self.debug = debug
        self.position = 0
        self.buffer_ = ''
        self.terminater = 0
        self.wrap = 1

    def parse(self, input_, start_rule=None):
        if isinstance(input_, Input):
            self.input_ = input_
        else:
            self.input_ = Input(input_)
        self.input_.open()

        self.buffer_ = self.input_.read()
        
        if not hasattr(self.grammar, '__module__'):
            try:
                imported_grammar = __import__(
                    '%s' % self.grammar,
                    {}, {}, ['Grammar']
                )
            except ImportError, err:
                raise # XXX
            self.grammar = imported_grammar.Grammar()

        if not start_rule:
            try:
                start_rule = self.grammar.tree.get(
                    'TOP', self.grammar.tree.get('+top', None)
                )
            except KeyError:
                raise # XXX

        if not hasattr(self.receiver, '__module__'):
            try:
                imported_receiver = __import__('%s' % self.receiver,
                        {}, {}, ['Receiver'])
            except ImportError, err:
                raise # XXX
            self.receiver = imported_receiver.Receiver()
        self.receiver.parser = self

        match = self.match(start_rule)
        if not match:
            return

        self.input_.close()

        data = self.receiver.data
        if data:
            return data
        return match

    def match(self, rule):
        if hasattr(self.receiver, 'initialize'):
            self.receiver.initialize()

        match = self.match_next({'.ref': rule})
        if not match or self.position < len(self.buffer_):
            self.throw_error("Parse document failed for some reason")
            return

        match = match[0]

        if hasattr(self.receiver, 'finalize'):
            self.receiver.finalize()

        if not match:
            match = { rule: [] }

        if rule == 'TOP':
            match = match['TOP']

        return match

    def match_next(self, next_):
        if '.sep' in next_:
            return self.match_next_with_sep(next_)

        quantity = next_.get('+qty', '1')
        assertion = next_.get('+asr', 0)
        rule = kind = None
        for kind in ['ref', 'rgx', 'all', 'any', 'err']:
            key = '.%s' % kind
            if key in next_:
                rule = next_[key]
                break

        match, position, count, method = (
            [], self.position, 0, "match_%s" % kind
        )

        return_ = getattr(self, method)(rule, parent=next_)
        while type(return_) == list:
            if not assertion:
                position = self.position
            count += 1
            match.extend(return_)
            if quantity in '1?':
                break
            return_ = getattr(self, method)(rule, parent=next_)

        if quantity in '+*':
            match = [match]
            self.position = position

        if count or quantity in '?*':
            result = 1
        else:
            result = 0
        if assertion == -1:
            a = 1
        else:
            a =0
        result = result ^ a

        if not result or assertion:
            self.position = position

        if '-skip' in next_:
            match = []

        if result:
            return match
        else:
            return False

    def match_next_with_sep(self, next_):
        quantity = next_.get('+qty', '1')
        rule = kind = None
        for kind in ['ref', 'rgx', 'all', 'any', 'err']:
            key = '.%s' % kind
            if key in next_:
                rule = next_[key]
                break

        separator = next_.get('.sep');
        sep_rule = sep_kind = None
        for sep_kind in ['ref', 'rgx', 'all', 'any', 'err']:
            key = '.%s' % sep_kind
            if key in separator:
                sep_rule = separator[key]
                break

        match, position, count, sep_count, method, sep_method = (
            [], self.position, 0, 0,
            "match_%s" % kind, "match_%s" % sep_kind
        )

        return_ = getattr(self, method)(rule, next_)
        while type(return_) == list:
            position = self.position
            count += 1
            match.extend(return_)
            return_ = getattr(self, sep_method)(sep_rule, separator)
            if type(return_) != list:
                break
            match.extend(return_)
            sep_count += 1
            return_ = getattr(self, method)(rule, next_)

        if not count:
            if quantity is '?':
                return [match]
            else:
                return False

        if count == sep_count:
            self.position = position

        if next_.get('-skip', None):
            return []

        return [match]

    def match_ref(self, ref, parent):
        rule = self.grammar.tree.get(ref, None)
        if not rule:
            raise "\n\n*** No grammar support for '%s'\n\n" % ref

        trace = bool(not('+asr' in rule) and self.debug)
        if trace:
            self.trace("try_%s" % ref)

        match = self.match_next(rule)
        if type(match) != list:
            if trace:
                self.trace("not_%s" % ref)
            return False

        # Call receiver callbacks
        if trace:
            self.trace("got_%s" % ref)
        if not('+asr' in rule) and not('-skip' in parent):
            callback = "got_%s" % ref
            try:
                sub = getattr(self.receiver, callback)
            except AttributeError:
                sub = None
            if (sub):
                match = [ sub(match[0]) ]
            elif (self.wrap and not('-pass' in parent)) or '-wrap' in parent:
                if match:
                    match = [ { ref: match[0] } ]
                else:
                    match = []

        return match


    def match_rgx(self, regexp, parent=None):
        start = self.position
        self.terminater += 1
        if start >= len(self.buffer_) and self.terminater > 1000:
            raise Exception(
                "Your grammar seems to not terminate at end of stream"
            )

        m = re.match(regexp, self.buffer_[start:])
        if not m:
            return False
        self.position += m.end()

        match = []
        match.extend(m.groups())
        if len(match) > 1:
            match = [match]

        return match

    def match_all(self, list_, parent=None):
        pos = self.position
        set_ = []
        len_ = 0

        for elem in list_:
            match = self.match_next(elem)
            if type(match) == list:
                set_.extend(match)
                len_ += 1
            else:
                self.position = pos
                return False

        if len_ > 1:
            set_ = [set_]
        return set_

    def match_any(self, list_, parent=None):

        for elem in list_:
            match = self.match_next(elem)
            if match:
                return match
        return False

    def match_err(self, error, parent=None):
        self.throw_error(error)

    def trace(self, action):
        if action.startswith('try_'):
            indent = 1
        else:
            indent = 0
        if not indent:
            self.indent -= 1
        # print STDERR ' ' x $self->{indent};
        print ' ' * self.indent,
        if indent:
            self.indent += 1
        snippet = self.buffer_[self.position:]
        if len(snippet) > 30:
            snippet = snippet[0:30]
        snippet = snippet.replace('\n', '\\n')
        # print STDERR sprintf("%-30s", $action) . ($indent ? " >$snippet<\n" : "\n");
        print "%-30s" % action,
        if indent:
            print " >%s<" % snippet
        else:
            print ""
        # print STDERR sprintf("%-30s", $action) . ($indent ? " >$snippet<\n" : "\n");

    def throw_error(self, msg):
        line = self.buffer_[0:self.position].count('\n') + 1
        column = self.position - self.buffer_.rfind("\n", 0, self.position)
        context = self.buffer_[self.position:50].replace('\n', '\\n')
        position = self.position
        error = """\
Error parsing Pegex document:
  msg: %(msg)s
  line: %(line)s
  column: %(column)s
  context: "%(context)s"
  position: %(position)s
...
""" % locals()
        if self.throw_on_error:
            raise Exception(error)
        self.error = error
        return False

