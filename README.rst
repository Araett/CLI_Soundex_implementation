CLI Soundex Implementation
==========================

Installation
------------

Requires:

- python 3.6+

Requirements:

All requirements and dependencies will install with a makefile::

    make install

Running
-------

bash:
    From `pipenv shell`::
        
        python soundex.py <path/to/file> <target_word>


`path/to/file` and `target_word` must be valid

Testing
-------

bash:
    From `pipenv shell` and root folder::

        pytest


