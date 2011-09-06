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

import re

input_ = __import__('pegex.input', {}, {}, ['Input'])
Input = input_.Input


class Parser():
    def __init__(self, grammar=None, receiver='pegex.ast', debug=False):
        self.grammar = grammar
        self.receiver = receiver
        self.debug = debug
        self.position = 0

    def parse(self, input, start_rule=None):
        if isinstance(input, Input):
            self.input = input
        else:
            self.input = Input(input)

        #self.buffer = self.input.read()
        self.buffer = self.input
        
        if not hasattr(self.grammar, '__module__'):
            try:
                print self.grammar
                imported_grammar = __import__('%s' % self.grammar,
                        {}, {}, ['Grammar'])
            except ImportError, err:
                raise # XXX
            self.grammar = imported_grammar.Grammar()

        if not start_rule:
            try:
                start_rule = self.grammar.tree.get('TOP', self.grammar.tree['+top'])
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

        print 'SR', start_rule
        match = self.match(start_rule)
        if not match:
            return

        self.input.close()

        data = self.receiver.data
        if data:
            return data
        return match

    def match(self, rule):
        if hasattr(self.receiver, 'begin'):
            self.receiver.begin()

        print 'R', rule
        match = self.match_ref(rule)
        if self.position < len(self.buffer_):
            self.throw_error("Parse document failed for some reason")
            return

        if hasattr(self.receiver, 'final'):
            self.receiver.final()

        return match

    def match_next(self, next_, state=None):

        has, not_, times = 0, 0, '1'

        mod = next_.get('+mod', None)
        if mod is'=':
            has = 1
        elif mod is '!':
            not_ = 1
        elif mod:
            times = mod

        rule = kind = None
        for kind in ['ref', 'rfx', 'all', 'any', 'err']:
            key = '.%s' % kind
            if key in next_:
                rule = next_[key]
                break

        if state and not(has or not_):
            self.callback("try", state, None)

        match, position, count, method = ([],  self.position, 0,
                'match_%s' % kind)

        print 'M, R', method, rule
        return_ = getattr(self, method)(rule)
        print 'R_', return_
        while return_:
            if not not_:
                position = self.position
            count += 1
            if times in '1?':
                match = return_
                break
            if return_ != IGNORE:
                match.append(return_)
            return_ = getattr(self, method)(rule)

        if count and times in '+*':
            self.position = position

        if count or times in '?*':
            result = 1
        else:
            result = 0
        result = result ^ not_

        if not result:
            self.position = position

        if state and not(has or not_):
            if result:
                 got = 'got'
            else:
                 got = 'not'
            self.callback(got, state, match)

        if not match:
            match = IGNORE

        if result:
            return match
        else:
            return False

    def match_ref(self, ref):
        try:
            return self.match_next(self.grammar.tree[ref], ref)
        except KeyError:
            self.throw_error("\n\n*** No grammar support for '%s'\n\n" % ref)

    def match_rgx(self, regexp):
        start = self.position
        m = re.match(regexp, self.buffer_[start:])
        if not m:
            return False
        self.position += m.end()

        match = {}
        index = 1
        for group in m.groups():
            match[index] = group

        return match;

    def match_all(self, list_):
        pos = self.position
        set_ = []

        for elem in list_:
            match = self.match_next(elem)
            if match:
                if match is not IGNORE:
                    set_.append(match)
            else:
                self.position = pos
                return False

        if len(list_) == 1:
            return set[0]
        else:
            return set


    def match_any(self, list_):

        for elem in list_:
            match = self.match_next(elem)
            if match:
                return match
        return False

    def match_err(self, error):
        self.throw_error(error)

    def callback(self, adj, rule, match):
        callback = '%s_%s' % (adj, rule)
        if self.debug:
            self.trace(callback)
        if adj is 'got':
            if hasattr(self.receiver, 'got'):
                match = self.receiver.got(rule, match)
            if hasattr(self.receiver, callback):
                match = getattr(self.receiver,
                        callback)(self.reciever, match)
            return match
        return 

    def trace(self, action):
        print action
    """
    sub trace {
        my $self = shift;
        my $action = shift;
        my $indent = ($action =~ /^try_/) ? 1 : 0;
        $self->{indent} ||= 0;
        $self->{indent}-- unless $indent;
        print STDERR ' ' x $self->{indent};
        $self->{indent}++ if $indent;
        my $snippet = substr($self->buffer, $self->position);
        $snippet = substr($snippet, 0, 30) . "..." if length $snippet > 30;
        $snippet =~ s/\n/\\n/g;
        print STDERR sprintf("%-30s", $action) . ($indent ? " >$snippet<\n" : "\n");
    }
    """

    def throw_error(self, msg):
        raise ParseException(msg)
    """
    sub throw_error {
        my $self = shift;
        my $msg = shift;
        my $line = @{[substr($self->buffer, 0, $self->position) =~ /(\n)/g]} + 1;
        my $context = substr($self->buffer, $self->position, 50);
        $context =~ s/\n/\\n/g;
        my $position = $self->position;
        my $error = <<"...";
    Error parsing Pegex document:
      msg: $msg
      line: $line
      context: "$context"
      position: $position
    ...
        if ($self->error eq 'die') {
            require Carp;
            Carp::croak($error);
        }
        elsif ($self->error eq 'live') {
            $@ = $error;
            return;
        }
        else {
            die "Invalid value for Pegex::Parser::error";
        }
    }
    """

