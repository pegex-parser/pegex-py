""""\
##
# name:      Pegex::Receiver
# abstract:  Pegex Receiver Base Class
# author:    Ingy dot Net <ingy@cpan.org>
# license:   perl
# copyright: 2011
"""


class Receiver(object):

    def __init__(self):
        self.parser = None
        self.data = None
