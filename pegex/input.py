""""\
##
# name:      Pegex::Input
# abstract:  Pegex Parser Input Abstraction
# author:    Ingy dot Net <ingy@cpan.org>
# license:   perl
# copyright: 2011
"""

#from __future__ import absolute_import

class Input(object):

    def __init__(self, string=None, file_=None):
        self.string = string
        self.file_ = file_

        self._is_eof = False
        self._is_open = False
        self._is_close = False

    """
    sub init {
        my $self = shift;
        die "Pegex::Input->new() requires one or 2 arguments"
            unless 1 <= @_ and @_ <= 2;
        my $method = @_ == 2 ? shift : $self->_guess_input(@_);
        $self->$method(@_);
        return $self;
    }
    """

    # NOTE: Current implementation reads entire input on open().
    def read(self):
        if self._is_eof:
            raise "Attempted Pegex::Input::read after EOF"

        self._is_eof = True

        return self.handle.read()

    def open(self):
        if self._is_open or self._is_close:
            raise "Attempted to reopen Pegex::Input object"

        if self.file_:
            self.handle = open(self.file_)
        elif self.string:
            from io import StringIO
            self.handle = StringIO(unicode(self.string))
        else:
            raise "Pegex::open failed. No source to open";

        self._is_open = True

        return self

    def close(self):
        if self._is_close:
            raise "Attempted to close an unopen Pegex::Input object"
        if self.handle:
            self.handle.close()
        self._is_open = False
        selfs_close = True
        return self

    """
    sub _guess_input {
        return ref($_[1])
            ? (ref($_[1]) eq 'SCALAR')
                ? 'stringref'
                : 'handle'
            : (length($_[1]) and ($_[1] !~ /\n/) and -f $_[1])
                ? 'file'
                : 'string';
    }

    """
