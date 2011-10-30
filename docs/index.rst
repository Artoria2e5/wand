Wand
====

Wand is a :mod:`ctypes`-based simple `MagickWand API`_ binding for Python. ::

    from wand.image import Image

    with Image(filename='mona-lisa.png') as img:
        print img.size
        for r in 1, 2, 3:
            with img.clone() as i:
                i.rotate_right()
                if r % 2:
                    i.sepia_tone()
                i.save('mona-lisa-{0}.png'.format(i))

You can install it from PyPI_ (and it requires MagickWand library):

.. sourcecode:: bash

   $ apt-get install libmagickwand-dev
   $ easy_install Wand

.. _MagickWand API: http://www.imagemagick.org/script/magick-wand.php
.. _PyPI: http://pypi.python.org/pypi/Wand


Why just another binding?
-------------------------

There are already many MagickWand API bindings for Python, however they
are lacking something we need:

- Pythonic and modern interfaces
- Good documentation
- Binding through :mod:`ctypes` (not C API) --- we are ready to go PyPy!
- Installation using :program:`pip` or :program:`easy_install`


Requirements
------------

- Python 2.6 or higher

  - CPython 2.6 or higher
  - PyPy 1.5 or higher

- MagickWand library

  - ``libmagickwand-dev`` for APT on Debian/Ubuntu
  - ``imagemagick`` for MacPorts/Homebrew on Mac
  - ``ImageMagick-devel`` for Yum on CentOS


User's guide
------------

.. toctree::
   :maxdepth: 2

   guide/resource
   changes


References
----------

.. toctree::
   :maxdepth: 2

   wand


Open source
-----------

Wand is an open source software to be used for StyleShare_ and written by
`Hong Minhee`_. The source code is distributed under MIT license and you can
find it at `GitHub repository`_. Check out now:

.. sourcecode:: bash

   $ git clone https://github.com/StyleShare/wand

If you find a bug, please notify to `our issue tracker`_. Pull requests
are always welcome!

Check out :doc:`changes` also.

.. _StyleShare: https://stylesha.re/
.. _Hong Minhee: http://dahlia.kr/
.. _GitHub repository: https://github.com/StyleShare/wand
.. _our issue tracker: https://github.com/StyleShare/wand/issues


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

