def get():
    info = {}
    info.update(
{ 'author': 'Ingy dot Net',
  'author_email': 'ingy@ingy.net',
  'classifiers': [ 'Development Status :: 2 - Pre-Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python',
                   'Topic :: Software Development',
                   'Topic :: System :: Software Distribution'],
  'description': 'This is your-package',
  'install_requires': ['pyyaml'],
  'long_description': 'thingy - Blah blah blah\n-----------------------\n\nInstallation\n------------\n\nUse::\n\n    > sudo pip install thingy\n\nor::\n\n    > sudo easy install thingy\n\nor::\n\n    > git clone git://github.com/you/thingy-py.git\n    > cd thingy-py\n    > sudo make install\n\nUsage\n-----\n\nDevelopment Status\n------------------\n\nCommunity\n---------\n\nAuthors\n-------\n\n* You Yourself <you@example.com>\n\nCopyright\n---------\n\nthingy is Copyright (c) 2010, You Yourself\n\nthingy is licensed under the New BSD License. See the LICENSE file.\n',
  'name': 'pegex',
  'packages': ['pegex'],
  'scripts': [],
  'url': 'http://www.cdent.org/',
  'version': '0.0.1'}
)
    return info
