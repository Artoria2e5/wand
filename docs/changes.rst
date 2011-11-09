Wand Changelog
==============

Version 0.1.7
-------------

To be released. Still alpha version.

 - Added :attr:`Image.mimetype <wand.image.Image.mimetype>` property.

Version 0.1.6
-------------

Released on October 31, 2011. Still alpha version.

- Removed a side effect of :class:`Image.make_blob()
  <wand.image.Image.make_blob>` method that changes the image format silently.
- Added :attr:`Image.format <wand.image.Image.format>` property.
- Added :meth:`Image.convert() <wand.image.Image.convert>` method.
- Fixed a bug about Python 2.6 compatibility.
- Use the internal representation of :c:type:`PixelWand` instead of
  the string representaion for :class:`~wand.color.Color` type.

Version 0.1.5
-------------

Released on October 28, 2011. Slightly mature alpha version.

- Now :class:`~wand.image.Image` can read Python file objects by ``file``
  keyword argument.
- Now :class:`Image.save() <wand.image.Image.save>` method can write into
  Python file objects by ``file`` keyword argument.
- :class:`Image.make_blob() <wand.image.Image.make_blob>`'s ``format``
  argument becomes omittable.

Version 0.1.4
-------------

Released on October 27, 2011. Hotfix of the malformed Python package.

Version 0.1.3
-------------

Released on October 27, 2011. Slightly mature alpha version.

- Pixel getter for :class:`~wand.image.Image`.
- Row getter for :class:`~wand.image.Image`.
- Mac compatibility.
- Windows compatibility.
- 64-bit processor compatibility.

Version 0.1.2
-------------

Released on October 16, 2011. Still alpha version.

- :class:`~wand.image.Image` implements iterable interface.
- Added `wand.color` module.
- Added the abstract base class of all Wand resource objects:
  :class:`wand.resource.Resource`.
- :class:`~wand.image.Image` implements slicing.
- Cropping :class:`~wand.image.Image` using its slicing operator.

Version 0.1.1
-------------

Released on October 4, 2011. Still alpha version.

- Now it handles errors and warnings properly and in natural way of Python.
- Added :meth:`Image.make_blob() <wand.image.Image.make_blob>` method.
- Added ``blob`` parameter into :class:`~wand.image.Image` constructor.
- Added :meth:`Image.resize() <wand.image.Image.resize>` method.
- Added :meth:`Image.save() <wand.image.Image.save>` method.
- Added :meth:`Image.clone() <wand.image.Image.clone>` method.
- Drawed `the pretty logo picture <_static/wand.png>`_
  (thanks to `Hyojin Choi <http://me2day.net/crocodile>`_).


Version 0.1.0
-------------

Released on October 1, 2011. Very alpha version.

