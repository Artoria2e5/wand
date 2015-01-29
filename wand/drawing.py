""":mod:`wand.drawing` --- Drawings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The module provides some vector drawing functions.

.. versionadded:: 0.3.0

"""
import collections
import ctypes
import numbers

from .api import library, MagickPixelPacket, PointInfo
from .color import Color
from .compat import binary, string_type, text, text_type, xrange
from .image import Image
from .resource import Resource
from .exceptions import WandLibraryVersionError

__all__ = ('CLIP_PATH_UNITS', 'FILL_RULE_TYPES', 'FONT_METRICS_ATTRIBUTES',
           'GRAVITY_TYPES', 'LINE_CAP_TYPES', 'LINE_JOIN_TYPES',
           'PAINT_METHOD_TYPES', 'TEXT_ALIGN_TYPES', 'TEXT_DECORATION_TYPES',
           'TEXT_DIRECTION_TYPES','Drawing', 'FontMetrics')


#: (:class:`collections.Sequence`) The list of clip path units
#:
#: - ``'undefined_path_units'``
#: - ``'user_space'``
#: - ``'user_space_on_use'``
#: - ``'object_bounding_box'``
CLIP_PATH_UNITS = ('undefined_path_units', 'user_space', 'user_space_on_use',
                   'object_bounding_box')

#: (:class:`collections.Sequence`) The list of text align types.
#:
#: - ``'undefined'``
#: - ``'left'``
#: - ``'center'``
#: - ``'right'``
TEXT_ALIGN_TYPES = 'undefined', 'left', 'center', 'right'

#: (:class:`collections.Sequence`) The list of text decoration types.
#:
#: - ``'undefined'``
#: - ``'no'``
#: - ``'underline'``
#: - ``'overline'``
#: - ``'line_through'``
TEXT_DECORATION_TYPES = ('undefined', 'no', 'underline', 'overline',
                         'line_through')

#: (:class:`collections.Sequence`) The list of text direction types.
#:
#: - ``'undefined'``
#: - ``'right_to_left'``
#: - ``'left_to_right'``
TEXT_DIRECTION_TYPES = ('undefined', 'right_to_left', 'left_to_right')

#: (:class:`collections.Sequence`) The list of text gravity types.
#:
#: - ``'forget'``
#: - ``'north_west'``
#: - ``'north'``
#: - ``'north_east'``
#: - ``'west'``
#: - ``'center'``
#: - ``'east'``
#: - ``'south_west'``
#: - ``'south'``
#: - ``'south_east'``
#: - ``'static'``
GRAVITY_TYPES = ('forget', 'north_west', 'north', 'north_east', 'west',
                 'center', 'east', 'south_west', 'south', 'south_east',
                 'static')

#: (:class:`collections.Sequence`) The list of fill-rule types.
#:
#: - ``'undefined'``
#: - ``'evenodd'``
#: - ``'nonzero'``
FILL_RULE_TYPES = ('undefined', 'evenodd', 'nonzero')

#: (:class:`collections.Sequence`) The attribute names of font metrics.
FONT_METRICS_ATTRIBUTES = ('character_width', 'character_height', 'ascender',
                           'descender', 'text_width', 'text_height',
                           'maximum_horizontal_advance', 'x1', 'y1', 'x2',
                           'y2', 'x', 'y')

#: The tuple subtype which consists of font metrics data.
FontMetrics = collections.namedtuple('FontMetrics', FONT_METRICS_ATTRIBUTES)

#: (:class:`collections.Sequence`) The list of LineCap types
#:
#: - ``'undefined;``
#: - ``'butt'``
#: - ``'round'``
#: - ``'square'``
LINE_CAP_TYPES = ('undefined', 'butt', 'round', 'square')

#: (:class:`collections.Sequence`) The list of LineJoin types
#:
#: - ``'undefined'``
#: - ``'miter'``
#: - ``'round'``
#: - ``'bevel'``
LINE_JOIN_TYPES = ('undefined', 'miter', 'round', 'bevel')


#: (:class:`collections.Sequence`) The list of paint method types.
#:
#: - ``'undefined'``
#: - ``'point'``
#: - ``'replace'``
#: - ``'floodfill'``
#: - ``'filltoborder'``
#: - ``'reset'``
PAINT_METHOD_TYPES = ('undefined', 'point', 'replace',
                      'floodfill', 'filltoborder', 'reset')


class Drawing(Resource):
    """Drawing object.  It maintains several vector drawing instructions
    and can get drawn into zero or more :class:`~wand.image.Image` objects
    by calling it.

    For example, the following code draws a diagonal line to the ``image``::

        with Drawing() as draw:
            draw.line((0, 0), image.size)
            draw(image)

    :param drawing: an optional drawing object to clone.
                    use :meth:`clone()` method rathan than this parameter
    :type drawing: :class:`Drawing`

    .. versionadded:: 0.3.0

    """

    c_is_resource = library.IsDrawingWand
    c_destroy_resource = library.DestroyDrawingWand
    c_get_exception = library.DrawGetException
    c_clear_exception = library.DrawClearException

    def __init__(self, drawing=None):
        with self.allocate():
            if not drawing:
                wand = library.NewDrawingWand()
            elif not isinstance(drawing, type(self)):
                raise TypeError('drawing must be a wand.drawing.Drawing '
                                'instance, not ' + repr(drawing))
            else:
                wand = library.CloneDrawingWand(drawing.resource)
            self.resource = wand

    def clone(self):
        """Copies a drawing object.

        :returns: a duplication
        :rtype: :class:`Drawing`

        """
        return type(self)(drawing=self)

    @property
    def clip_path(self):
      """(:class:`basestring`) The current clip path. It also can be set.

      .. versionadded:: 0.4.0

      """
      return text(library.DrawGetClipPath(self.resource))

    @clip_path.setter
    def clip_path(self, path):
      if not isinstance(path, string_type):
        raise TypeError('expected a string, not ' + repr(path))
      okay = library.DrawSetClipPath(self.resource, binary(path))
      if okay == 0:
        raise ValueError('Clip path not understood')

    @property
    def clip_rule(self):
      """(:class:`basestring`) The current clip rule. It also can be set.
      It's a string value from :const:`FILL_RULE_TYPES` list.

      .. versionadded:: 0.4.0
      """
      clip_rule = library.DrawGetClipRule(self.resource)
      return FILL_RULE_TYPES[clip_rule]

    @clip_rule.setter
    def clip_rule(self, clip_rule):
        if not isinstance(clip_rule, string_type):
            raise TypeError('expected a string, not ' + repr(clip_rule))
        elif clip_rule not in FILL_RULE_TYPES:
            raise ValueError('expected a string from FILE_RULE_TYPES, not' +
                             repr(clip_rule))
        library.DrawSetClipRule(self.resource,
                                FILL_RULE_TYPES.index(clip_rule))

    @property
    def clip_units(self):
      """(:class:`basestring`) The current clip units. It also can be set.
      It's a string value from :const:`CLIP_PATH_UNITS` list.

      .. versionadded:: 0.4.0
      """
      clip_unit = library.DrawGetClipUnits(self.resource)
      return CLIP_PATH_UNITS[clip_unit]

    @clip_units.setter
    def clip_units(self, clip_unit):
        if not isinstance(clip_unit, string_type):
            raise TypeError('expected a string, not ' + repr(clip_unit))
        elif clip_unit not in CLIP_PATH_UNITS:
            raise ValueError('expected a string from CLIP_PATH_UNITS, not' +
                             repr(clip_unit))
        library.DrawSetClipUnits(self.resource,
                                CLIP_PATH_UNITS.index(clip_unit))

    @property
    def font(self):
        """(:class:`basestring`) The current font name.  It also can be set."""
        return text(library.DrawGetFont(self.resource))

    @font.setter
    def font(self, font):
        if not isinstance(font, string_type):
            raise TypeError('expected a string, not ' + repr(font))
        library.DrawSetFont(self.resource, binary(font))

    @property
    def font_size(self):
        """(:class:`numbers.Real`) The font size.  It also can be set."""
        return library.DrawGetFontSize(self.resource)

    @font_size.setter
    def font_size(self, size):
        if not isinstance(size, numbers.Real):
            raise TypeError('expected a numbers.Real, but got ' + repr(size))
        elif size < 0.0:
            raise ValueError('cannot be less then 0.0, but got ' + repr(size))
        library.DrawSetFontSize(self.resource, size)

    @property
    def fill_color(self):
        """(:class:`~wand.color.Color`) The current color to fill.
        It also can be set.

        """
        pixel = library.NewPixelWand()
        library.DrawGetFillColor(self.resource, pixel)
        size = ctypes.sizeof(MagickPixelPacket)
        buffer = ctypes.create_string_buffer(size)
        library.PixelGetMagickColor(pixel, buffer)
        return Color(raw=buffer)

    @fill_color.setter
    def fill_color(self, color):
        if not isinstance(color, Color):
            raise TypeError('color must be a wand.color.Color object, not ' +
                            repr(color))
        with color:
            library.DrawSetFillColor(self.resource, color.resource)

    @property
    def fill_opacity(self):
        """(:class:`~numbers.Real`) The current fill opacity.
        It also can be set.

        .. versionadded:: 0.4.0
        """
        return library.DrawGetFillOpacity(self.resource)

    @fill_opacity.setter
    def fill_opacity(self, opacity):
        if not isinstance(opacity, numbers.Real):
            raise TypeError('opacity must be a double, not ' +
                            repr(opacity))
        library.DrawSetFillOpacity(self.resource, opacity)

    @property
    def fill_rule(self):
        """(:class:`basestring`) The current fill rule. It can also be set.
        It's a string value from :const:`FILL_RULE_TYPES` list.

        .. versionadded:: 0.4.0
        """
        fill_rule_index = library.DrawGetFillRule(self.resource)
        if fill_rule_index not in FILL_RULE_TYPES:
            self.raise_exception()
        return text(FILL_RULE_TYPES[fill_rule_index])

    @fill_rule.setter
    def fill_rule(self, fill_rule):
        if not isinstance(fill_rule, string_type):
            raise TypeError('expected a string, not ' + repr(fill_rule))
        elif fill_rule not in FILL_RULE_TYPES:
            raise ValueError('expected a string from FILE_RULE_TYPES, not' +
                             repr(fill_rule))
        library.DrawSetFillRule(self.resource,
                                FILL_RULE_TYPES.index(fill_rule))

    @property
    def stroke_antialias(self):
        """(:class:`bool`) Controls whether stroked outlines are antialiased.
        Stroked outlines are antialiased by default. When antialiasing is
        disabled stroked pixels are thresholded to determine if the stroke color
        or underlying canvas color should be used.

        It also can be set.

        .. versionadded:: 0.4.0

        """
        stroke_antialias = library.DrawGetStrokeAntialias(self.resource)
        return bool(stroke_antialias)

    @stroke_antialias.setter
    def stroke_antialias(self, stroke_antialias):
        library.DrawSetStrokeAntialias(self.resource, bool(stroke_antialias))

    @property
    def stroke_color(self):
        """(:class:`~wand.color.Color`) The current color of stroke.
        It also can be set.

        .. versionadded:: 0.3.3
        
        """
        pixel = library.NewPixelWand()
        library.DrawGetStrokeColor(self.resource, pixel)
        size = ctypes.sizeof(MagickPixelPacket)
        buffer = ctypes.create_string_buffer(size)
        library.PixelGetMagickColor(pixel, buffer)
        return Color(raw=buffer)

    @stroke_color.setter
    def stroke_color(self, color):
        if not isinstance(color, Color):
            raise TypeError('color must be a wand.color.Color object, not ' + 
                            repr(color))
        with color:
            library.DrawSetStrokeColor(self.resource, color.resource)

    @property
    def stroke_dash_array(self):
        """(:class:`~collections.Sequence`) - (:class:`numbers.Real`) An array
        representing the pattern of dashes & gaps used to stroke paths.
        It also can be set.

        .. versionadded:: 0.4.0"""
        number_elements = ctypes.c_size_t(0)
        dash_array = library.DrawGetStrokeDashArray(self.resource,
                                                    ctypes.byref(number_elements))
        return [float(dash_array[i]) for i in xrange(number_elements.value)]

    @stroke_dash_array.setter
    def stroke_dash_array(self, dash_array):
        dash_array_l = len(dash_array)
        dash_array_p = (ctypes.c_double * dash_array_l)(*dash_array)
        library.DrawSetStrokeDashArray(self.resource, dash_array_l, dash_array_p)

    @property
    def stroke_dash_offset(self):
        """(:class:`numbers.Real`) The stroke dash offset. It also can be set.

        .. versionadded:: 0.4.0
        """
        return library.DrawGetStrokeDashOffset(self.resource)

    @stroke_dash_offset.setter
    def stroke_dash_offset(self, offset):
        library.DrawSetStrokeDashOffset(self.resource, float(offset))

    @property
    def stroke_line_cap(self):
        """(:class:`basestring`) The stroke line cap. It also can be set.

        .. versionadded:: 0.4.0
        """
        line_cap_index = library.DrawGetStrokeLineCap(self.resource)
        if line_cap_index not in LINE_CAP_TYPES:
            self.raise_exception()
        return text(LINE_CAP_TYPES[line_cap_index])

    @stroke_line_cap.setter
    def stroke_line_cap(self, line_cap):
        if not isinstance(line_cap, string_type):
            raise TypeError('expected a string, not ' + repr(line_cap))
        elif line_cap not in LINE_CAP_TYPES:
            raise ValueError('expected a string from LINE_CAP_TYPES, not' +
                             repr(line_cap))
        library.DrawSetStrokeLineCap(self.resource,
                                LINE_CAP_TYPES.index(line_cap))

    @property
    def stroke_line_join(self):
        """(:class:`basestring`) The stroke line join. It also can be set.

        .. versionadded:: 0.4.0
        """
        line_join_index = library.DrawGetStrokeLineJoin(self.resource)
        if line_join_index not in LINE_JOIN_TYPES:
            self.raise_exception()
        return text(LINE_JOIN_TYPES[line_join_index])

    @stroke_line_join.setter
    def stroke_line_join(self, line_join):
        if not isinstance(line_join, string_type):
            raise TypeError('expected a string, not ' + repr(line_join))
        elif line_join not in LINE_JOIN_TYPES:
            raise ValueError('expected a string from LINE_JOIN_TYPES, not' +
                             repr(line_join))
        library.DrawSetStrokeLineJoin(self.resource,
                                LINE_JOIN_TYPES.index(line_join))

    @property
    def stroke_miter_limit(self):
        """(:class:`~numbers.Integral`) The current miter limit.
        It also can be set.

        .. versionadded:: 0.4.0
        """
        return library.DrawGetStrokeMiterLimit(self.resource)

    @stroke_miter_limit.setter
    def stroke_miter_limit(self, miter_limit):
        if not isinstance(miter_limit, numbers.Integral):
            raise TypeError('opacity must be a integer, not ' +
                            repr(miter_limit))
        library.DrawSetStrokeMiterLimit(self.resource, miter_limit)

    @property
    def stroke_opacity(self):
        """(:class:`~numbers.Real`) The current stroke opacity.
        It also can be set.

        .. versionadded:: 0.4.0
        """
        return library.DrawGetStrokeOpacity(self.resource)

    @stroke_opacity.setter
    def stroke_opacity(self, opacity):
        if not isinstance(opacity, numbers.Real):
            raise TypeError('opacity must be a double, not ' +
                            repr(opacity))
        library.DrawSetStrokeOpacity(self.resource, opacity)

    @property
    def stroke_width(self):
        """(:class:`numbers.Real`) The stroke width.  It also can be set.

        .. versionadded:: 0.3.3

        """
        return library.DrawGetStrokeWidth(self.resource)

    @stroke_width.setter
    def stroke_width(self, width):
        if not isinstance(width, numbers.Real):
           raise TypeError('expected a numbers.Real, but got ' + repr(width)) 
        elif width < 0.0:
           raise ValueError('cannot be less then 0.0, but got ' + repr(width))
        library.DrawSetStrokeWidth(self.resource, width)

    @property
    def text_alignment(self):
        """(:class:`basestring`) The current text alignment setting.
        It's a string value from :const:`TEXT_ALIGN_TYPES` list.
        It also can be set.

        """
        text_alignment_index = library.DrawGetTextAlignment(self.resource)
        if not text_alignment_index:
            self.raise_exception()
        return text(TEXT_ALIGN_TYPES[text_alignment_index])

    @text_alignment.setter
    def text_alignment(self, align):
        if not isinstance(align, string_type):
            raise TypeError('expected a string, not ' + repr(align))
        elif align not in TEXT_ALIGN_TYPES:
            raise ValueError('expected a string from TEXT_ALIGN_TYPES, not ' +
                             repr(align))
        library.DrawSetTextAlignment(self.resource,
                                     TEXT_ALIGN_TYPES.index(align))

    @property
    def text_antialias(self):
        """(:class:`bool`) The boolean value which represents whether
        antialiasing is used for text rendering.  It also can be set to
        ``True`` or ``False`` to switch the setting.

        """
        result = library.DrawGetTextAntialias(self.resource)
        return bool(result)

    @text_antialias.setter
    def text_antialias(self, value):
        library.DrawSetTextAntialias(self.resource, bool(value))

    @property
    def text_decoration(self):
        """(:class:`basestring`) The text decoration setting, a string
        from :const:`TEXT_DECORATION_TYPES` list.  It also can be set.

        """
        text_decoration_index = library.DrawGetTextDecoration(self.resource)
        if not text_decoration_index:
            self.raise_exception()
        return text(TEXT_DECORATION_TYPES[text_decoration_index])

    @text_decoration.setter
    def text_decoration(self, decoration):
        if not isinstance(decoration, string_type):
            raise TypeError('expected a string, not ' + repr(decoration))
        elif decoration not in TEXT_DECORATION_TYPES:
            raise ValueError('expected a string from TEXT_DECORATION_TYPES, '
                             'not ' + repr(decoration))
        library.DrawSetTextDecoration(self.resource,
                                      TEXT_DECORATION_TYPES.index(decoration))

    @property
    def text_direction(self):
      """(:class:`basestring`) The text direction setting. a string
      from :const:`TEXT_DIRECTION_TYPES` list. It also can be set."""
      text_direction_index = library.DrawGetTextDirection(self.resource)
      if not text_direction_index:
        self.raise_exception()
      return text(TEXT_DIRECTION_TYPES[text_direction_index])

    @text_direction.setter
    def text_direction(self, direction):
      if not isinstance(direction, string_type):
        raise TypeError('expected a string, not ' + repr(direction))
      elif direction not in TEXT_DIRECTION_TYPES:
        raise ValueError('expected a string from TEXT_DIRECTION_TYPES, '
                         'not ' + repr(direction))
      library.DrawSetTextDirection(self.resource,
                                   TEXT_DIRECTION_TYPES.index(direction))

    @property
    def text_encoding(self):
        """(:class:`basestring`) The internally used text encoding setting.
        Although it also can be set, but it's not encouraged.

        """
        return text(library.DrawGetTextEncoding(self.resource))

    @text_encoding.setter
    def text_encoding(self, encoding):
        if encoding is not None and not isinstance(encoding, string_type):
            raise TypeError('expected a string, not ' + repr(encoding))
        elif encoding is None:
            # encoding specify an empty string to set text encoding
            # to system's default.
            encoding = b''
        else:
            encoding = binary(encoding)
        library.DrawSetTextEncoding(self.resource, encoding)

    @property
    def text_interline_spacing(self):
        """(:class:`numbers.Real`) The setting of the text line spacing.
        It also can be set.

        """
        if library.DrawGetTextInterlineSpacing is None:
            raise WandLibraryVersionError('The installed version of ImageMagick does not support this feature')
        return library.DrawGetTextInterlineSpacing(self.resource)

    @text_interline_spacing.setter
    def text_interline_spacing(self, spacing):
        if library.DrawSetTextInterlineSpacing is None:
            raise WandLibraryVersionError('The installed version of ImageMagick does not support this feature')
        if not isinstance(spacing, numbers.Real):
            raise TypeError('expected a numbers.Real, but got ' + repr(spacing))
        library.DrawSetTextInterlineSpacing(self.resource, spacing)

    @property
    def text_interword_spacing(self):
        """(:class:`numbers.Real`) The setting of the word spacing.
        It also can be set.

        """
        return library.DrawGetTextInterwordSpacing(self.resource)

    @text_interword_spacing.setter
    def text_interword_spacing(self, spacing):
        if not isinstance(spacing, numbers.Real):
            raise TypeError('expeted a numbers.Real, but got ' + repr(spacing))
        library.DrawSetTextInterwordSpacing(self.resource, spacing)

    @property
    def text_kerning(self):
        """(:class:`numbers.Real`) The setting of the text kerning.
        It also can be set.

        """
        return library.DrawGetTextKerning(self.resource)

    @text_kerning.setter
    def text_kerning(self, kerning):
        if not isinstance(kerning, numbers.Real):
            raise TypeError('expected a numbers.Real, but got ' + repr(kerning))
        library.DrawSetTextKerning(self.resource, kerning)

    @property
    def text_under_color(self):
        """(:class:`~wand.color.Color`) The color of a background rectangle
        to place under text annotations.  It also can be set.

        """
        pixel = library.NewPixelWand()
        library.DrawGetTextUnderColor(self.resource, pixel)
        size = ctypes.sizeof(MagickPixelPacket)
        buffer = ctypes.create_string_buffer(size)
        library.PixelGetMagickColor(pixel, buffer)
        return Color(raw=buffer)

    @text_under_color.setter
    def text_under_color(self, color):
        if not isinstance(color, Color):
            raise TypeError('expected a wand.color.Color object, not ' +
                            repr(color))
        with color:
            library.DrawSetTextUnderColor(self.resource, color.resource)

    @property
    def vector_graphics(self):
      """(:class:`basestring`) The XML text of the Vector Graphics. It also
      can be set. The drawing-wand XML is experimental, and subject to change.

      Setting this property to None will reset all vector graphic properties to
      the default state.

      .. versionadded:: 0.4.0

      """
      vector_graphics_p = library.DrawGetVectorGraphics(self.resource)
      vector_graphics = ctypes.create_string_buffer(vector_graphics_p)
      xml = text(vector_graphics.value);
      return "<drawing-wand>" + xml + "</drawing-wand>"

    @vector_graphics.setter
    def vector_graphics(self, vector_graphics):
      if vector_graphics is not None and not isinstance(vector_graphics,
                                                        string_type):
          raise TypeError('expected a string, not ' + repr(vector_graphics))
      elif vector_graphics is None:
          # Reset all vector graphic properties on drawing wand.
          library.DrawResetVectorGraphics(self.resource)
      else:
          vector_graphics = binary(vector_graphics)
          okay = library.DrawSetVectorGraphics(self.resource, vector_graphics)
          if okay == 0:
            raise ValueError("Vector graphic not understood.")

    @property
    def gravity(self):
        """(:class:`basestring`) The text placement gravity used when
        annotating with text.  It's a string from :const:`GRAVITY_TYPES`
        list.  It also can be set.

        """
        gravity_index = library.DrawGetGravity(self.resource)
        if not gravity_index:
            self.raise_exception()
        return text(GRAVITY_TYPES[gravity_index])

    @gravity.setter
    def gravity(self, value):
        if not isinstance(value, string_type):
            raise TypeError('expected a string, not ' + repr(value))
        elif value not in GRAVITY_TYPES:
            raise ValueError('expected a string from GRAVITY_TYPES, not '
                             + repr(value))
        library.DrawSetGravity(self.resource, GRAVITY_TYPES.index(value))

    def clear(self):
        library.ClearDrawingWand(self.resource)

    def draw(self, image):
        """Renders the current drawing into the ``image``.  You can simply
        call :class:`Drawing` instance rather than calling this method.
        That means the following code which calls :class:`Drawing` object
        itself::

            drawing(image)

        is equivalent to the following code which calls :meth:`draw()` method::

            drawing.draw(image)

        :param image: the image to be drawn
        :type image: :class:`~wand.image.Image`

        """
        if not isinstance(image, Image):
            raise TypeError('image must be a wand.image.Image instance, not '
                            + repr(image))
        res = library.MagickDrawImage(image.wand, self.resource)
        if not res:
            self.raise_exception()

    def arc(self, start, end, degree):
        """Draws a arc using the current :attr:`stroke_color`,
        :attr:`stroke_width`, and :attr:`fill_color`.

        :param start: (:class:`~numbers.Real`, :class:`numbers.Real`)
                      pair which represents starting x and y of the arc
        :type start: :class:`~collections.Sequence`
        :param end: (:class:`~numbers.Real`, :class:`numbers.Real`)
                      pair which represents ending x and y of the arc
        :type end: :class:`~collections.Sequence`
        :param degree: (:class:`~numbers.Real`, :class:`numbers.Real`)
                      pair which represents starting degree, and ending degree
        :type degree: :class:`~collections.Sequence`

        .. versionadded:: 0.4.0
        """

        start_x, start_y = start
        end_x, end_y = end
        degree_start, degree_end = degree
        library.DrawArc(self.resource,
                        float(start_x), float(start_y),
                        float(end_x), float(end_y),
                        float(degree_start), float(degree_end))

    def circle(self, origin, perimeter):
        """Draws a circle from ``origin`` to ``perimeter``

        :param origin: (:class:`~numbers.Real`, :class:`numbers.Real`)
                       pair which represents origin x and y of circle
        :type origin: :class:`collections.Sequence`
        :param perimeter: (:class:`~numbers.Real`, :class:`numbers.Real`)
                       pair which represents perimeter x and y of circle
        :type perimeter: :class:`collections.Sequence`

        .. versionadded:: 0.4.0
        """

        origin_x, origin_y = origin
        perimeter_x, perimeter_y = perimeter
        library.DrawCircle(self.resource,
                           float(origin_x), float(origin_y), # origin
                           float(perimeter_x), float(perimeter_y)) # perimeter

    def color(self, x=None, y=None, paint_method='undefined'):
        """Draws a color on the image using current fill color, starting
        at specified position & method.

        Available methods are:

        - ``'undefined'``
        - ``'point'``
        - ``'replace'``
        - ``'floodfill'``
        - ``'filltoborder'``
        - ``'reset'``

        .. versionadded:: 0.4.0
        """
        if x is None or y is None:
            raise TypeError('Both x & y coordinates need to be defined')
        if not isinstance(paint_method, string_type):
            raise TypeError('expected a string, not ' + repr(paint_method))
        elif paint_method not in PAINT_METHOD_TYPES:
            raise ValueError('expected a string from PAINT_METHOD_TYPES, not ' +
                             repr(paint_method))
        library.DrawColor(self.resource, float(x), float(y),
                          PAINT_METHOD_TYPES.index(paint_method))

    def ellipse(self, origin, radius, rotation=(0,360)):
        """Draws a ellipse at ``origin`` with independent x & y ``radius``.
        Ellipse can be partial by setting start & end ``rotation``.

        :param origin: (:class:`~numbers.Real`, :class:`numbers.Real`)
                       pair which represents origin x and y of circle
        :type origin: :class:`collections.Sequence`
        :param radius: (:class:`~numbers.Real`, :class:`numbers.Real`)
                       pair which represents radius x and radius y of circle
        :type radius: :class:`collections.Sequence`
        :param rotation: (:class:`~numbers.Real`, :class:`numbers.Real`)
                       pair which represents start and end of ellipse. Default (0,360) 
        :type rotation: :class:`collections.Sequence`

        .. versionadded:: 0.4.0
        """
        origin_x, origin_y = origin
        radius_x, radius_y = radius
        rotation_start, rotation_end = rotation
        library.DrawEllipse(self.resource,
                            float(origin_x), float(origin_y), # origin
                            float(radius_x), float(radius_y), # radius
                            float(rotation_start), float(rotation_end))

    def line(self, start, end):
        """Draws a line ``start`` to ``end``.

        :param start: (:class:`~numbers.Integral`, :class:`numbers.Integral`)
                      pair which represents starting x and y of the line
        :type start: :class:`collections.Sequence`
        :param end: (:class:`~numbers.Integral`, :class:`numbers.Integral`)
                    pair which represents ending x and y of the line
        :type end: :class:`collections.Sequence`

        """
        start_x, start_y = start
        end_x, end_y = end
        library.DrawLine(self.resource,
                         int(start_x), int(start_y),
                         int(end_x), int(end_y))

    def matte(self, x=None, y=None, paint_method='undefined'):
        """Paints on the image's opacity channel in order to set effected pixels
        to transparent.

         To influence the opacity of pixels. The available methods are:

        - ``'undefined'``
        - ``'point'``
        - ``'replace'``
        - ``'floodfill'``
        - ``'filltoborder'``
        - ``'reset'``

        .. versionadded:: 0.4.0
        """
        if x is None or y is None:
            raise TypeError('Both x & y coordinates need to be defined')
        if not isinstance(paint_method, string_type):
            raise TypeError('expected a string, not ' + repr(paint_method))
        elif paint_method not in PAINT_METHOD_TYPES:
            raise ValueError('expected a string from PAINT_METHOD_TYPES, not ' +
                             repr(paint_method))
        library.DrawMatte(self.resource, float(x), float(y),
                          PAINT_METHOD_TYPES.index(paint_method))

    def path_close(self):
        """Adds a path element to the current path which closes
        the current subpath by drawing a straight line from the current point
        to the current subpath's most recent starting point.

        .. versionadded:: 0.4.0
        """
        library.DrawPathClose(self.resource)
        return self

    def path_curve(self, to=None, controls=None, smooth=False, relative=False):
        """Draws a cubic Bezier curve from the current point to given ``to``
        (x,y) coordinate using ``controls`` points at the beginning & end of the
        curve. If ``smooth`` is set to True, only one ``controls`` is expected
        and the previous control is used, else two pair of coordinates are
        expected to define the control points. The ``to`` coordinate then
        becomes the new current point.

        :param to: (:class:`~numbers.Real`, :class:`numbers.Real`)
                      pair which represents coordinates to draw to.
        :type to: :class:`collections.Sequence`
        :param controls: (:class:`~numbers.Real`, :class:`numbers.Real`)
                      coordinate to used to influence curve
        :type controls: :class:`collections.Sequence`
        :param smooth: :class:`bool` assume last defined control coordinate
        :type smooth: :class:`bool`
        :param relative: :class:`bool`
                    treat given coordinates as relative to current point
        :type relative: :class:`bool`

        .. versionadded:: 0.4.0
        """
        if to is None:
            raise TypeError('to is missing')
        if controls is None:
            raise TypeError('controls is missing')
        x, y = to
        if smooth:
            x2, y2 = controls
        else:
            (x1, y1), (x2, y2) = controls

        if smooth:
            if relative:
                library.DrawPathCurveToSmoothRelative(self.resource,
                                                      x2, y2, x, y)
            else :
                library.DrawPathCurveToSmoothAbsolute(self.resource,
                                                      x2, y2, x, y)
        else:
            if relative:
                library.DrawPathCurveToRelative(self.resource,
                                                x1, y1, x2, y2, x, y)
            else :
                library.DrawPathCurveToAbsolute(self.resource,
                                                x1, y1, x2, y2, x, y)
        return self

    def path_curve_to_quadratic_bezier(self, to=None, control=None,
                                    smooth=False, relative=False):
        """Draws a quadratic Bezier curve from the current point to given
        ``to`` coordinate. The control point is assumed to be the reflection of
        the control point on the previous command if ``smooth`` is True, else a
        pair of ``control`` coordinates must be given. Each` coordinates can be
        relative, or absolute, to the current point by setting the ``relative``
        flag. The ``to`` coordinate then becomes the new current point, and the
        ``control`` coordinate will be assumed when called again when ``smooth``
        is set to true.

        :param to: (:class:`~numbers.Real`, :class:`numbers.Real`)
                      pair which represents coordinates to draw to.
        :type to: :class:`collections.Sequence`
        :param control: (:class:`~numbers.Real`, :class:`numbers.Real`)
                      coordinate to used to influence curve
        :type control: :class:`collections.Sequence`
        :param smooth: :class:`bool` assume last defined control coordinate
        :type smooth: :class:`bool`
        :param relative: :class:`bool`
                    treat given coordinates as relative to current point
        :type relative: :class:`bool`

        .. versionadded:: 0.4.0
        """
        if to is None:
            raise TypeError('to is missing')
        x, y = to

        if smooth:
            if relative:
                library.DrawPathCurveToQuadraticBezierSmoothRelative(self.resource,
                                                                     float(x),
                                                                     float(y))
            else:
                library.DrawPathCurveToQuadraticBezierSmoothAbsolute(self.resource,
                                                                     float(x),
                                                                     float(y))
        else:
            if control is None:
                raise TypeError('control is missing')
            x1, y1 = control
            if relative:
                library.DrawPathCurveToQuadraticBezierRelative(self.resource,
                                                               float(x1), float(y1),
                                                               float(x), float(y))
            else:
                library.DrawPathCurveToQuadraticBezierAbsolute(self.resource,
                                                               float(x1), float(y1),
                                                               float(x), float(y))
        return self

    def path_elliptic_arc(self, to=None, radius=None, rotation=0.0,
                          large_arc=False, clockwise=False, relative=False):
        """Draws an elliptical arc from the current point to given ``to``
        coordinates. The ``to`` coordinates can be relative, or absolute, to the
        current point by setting the ``relative`` flag. The size and orientation
        of the ellipse are defined by two radii (rx, ry) in ``radius`` and an
        ``rotation`` parameters, which indicates how the ellipse as a whole is
        rotated relative to the current coordinate system. The center of the
        ellipse is calculated automagically to satisfy the constraints imposed
        by the other parameters. ``large_arc`` and ``clockwise`` contribute to
        the automatic calculations and help determine how the arc is drawn.
        If ``large_arc`` is True then draw the larger of the available arcs.
        If ``clockwise`` is true, then draw the arc matching a clock-wise
        rotation.

        :param to: (:class:`~numbers.Real`, :class:`numbers.Real`)
                      pair which represents coordinates to draw to.
        :type to: :class:`collections.Sequence`
        :param radius: (:class:`~numbers.Real`, :class:`numbers.Real`)
                      pair which represents the radii of the ellipse to draw
        :type radius: :class:`collections.Sequence`
        :param rotate: :class:`~numbers.Real` degree to rotate ellipse on x-axis
        :type rotate: :class:`~numbers.Real`
        :param large_arc: :class:`bool` draw largest available arc
        :type large_arc: :class:`bool`
        :param clockwise: :class:`bool`
                    draw arc path clockwise from start to target
        :type clockwise: :class:`bool`
        :param relative: :class:`bool`
                    treat given coordinates as relative to current point
        :type relative: :class:`bool`

        .. versionadded:: 0.4.0
        """
        if to is None:
            raise TypeError('to is missing')
        if radius is None:
            raise TypeError('radius is missing')
        x, y = to
        rx, ry = radius
        if relative:
            library.DrawPathEllipticArcRelative(self.resource, float(rx), float(ry),
                                                float(rotation), bool(large_arc),
                                                bool(clockwise), float(x), float(y))
        else:
            library.DrawPathEllipticArcAbsolute(self.resource, float(rx), float(ry),
                                                float(rotation), bool(large_arc),
                                                bool(clockwise), float(x), float(y))
        return self

    def path_finish(self):
        """Terminates the current path.

        .. versionadded:: 0.4.0"""
        library.DrawPathFinish(self.resource)
        return self

    def path_line(self, to=None, relative=False):
        """Draws a line path from the current point to the given ``to``
        coordinate. The ``to`` coordinates can be relative, or absolute, to the
        current point by setting the ``relative`` flag. The coordinate then
        becomes the new current point.

        :param to: (:class:`~numbers.Real`, :class:`numbers.Real`)
                      pair which represents coordinates to draw to.
        :type to: :class:`collections.Sequence`
        :param relative: :class:`bool`
                    treat given coordinates as relative to current point
        :type relative: :class:`bool`

        .. versionadded:: 0.4.0
        """
        if to is None:
            raise TypeError('to is missing')
        x, y = to
        if relative:
            library.DrawPathLineToRelative(self.resource, float(x), float(y))
        else:
            library.DrawPathLineToAbsolute(self.resource, float(x), float(y))
        return self

    def path_horizontal_line(self, x=None, relative=False):
        """Draws a horizontal line path from the current point to the target
        point. Given ``x`` parameter can be relative, or absolute, to the
        current point by setting the ``relative`` flag. The target point then
        becomes the new current point.

        :param x: :class:`~numbers.Real`
                      x-axis point to draw to.
        :type x: :class:`~numbers.Real`
        :param relative: :class:`bool`
                    treat given point as relative to current point
        :type relative: :class:`bool`

        .. versionadded:: 0.4.0
        """
        if x is None:
            raise TypeError('x is missing')
        if relative:
            library.DrawPathLineToHorizontalRelative(self.resource, float(x))
        else:
            library.DrawPathLineToHorizontalAbsolute(self.resource, float(x))
        return self

    def path_vertical_line(self, y=None, relative=False):
        """Draws a vertical line path from the current point to the target point.
        Given ``y`` parameter can be relative, or absolute, to the current point
        by setting the ``relative`` flag. The target point then becomes the new
        current point.

        :param y: :class:`~numbers.Real`
                      y-axis point to draw to.
        :type y: :class:`~numbers.Real`
        :param relative: :class:`bool`
                    treat given point as relative to current point
        :type relative: :class:`bool`

        .. versionadded:: 0.4.0
        """
        if y is None:
            raise TypeError('y is missing')
        if relative:
            library.DrawPathLineToVerticalRelative(self.resource, float(y))
        else:
            library.DrawPathLineToVerticalAbsolute(self.resource, float(y))
        return self

    def path_move(self, to=None, relative=False):
        """Starts a new sub-path at the given coordinates. Given ``to`` parameter
        can be relative, or absolute, by setting the ``relative`` flag.

        :param to: (:class:`~numbers.Real`, :class:`numbers.Real`)
                      pair which represents coordinates to draw to.
        :type to: :class:`collections.Sequence`
        :param relative: :class:`bool`
                    treat given coordinates as relative to current point
        :type relative: :class:`bool`

        .. versionadded:: 0.4.0
        """
        if to is None:
            raise TypeError('to is missing')
        x, y = to
        if relative:
            library.DrawPathMoveToRelative(self.resource, float(x), float(y))
        else:
            library.DrawPathMoveToAbsolute(self.resource, float(x), float(y))
        return self

    def path_start(self):
        """Declares the start of a path drawing list which is terminated by a
        matching :meth:`path_finish()` command. All other `path_*` commands
        must be enclosed between a :meth:`path_start()` and a
        :meth:`path_finish()` command. This is because path drawing commands
        are subordinate commands and they do not function by themselves.

        .. versionadded:: 0.4.0
        """
        library.DrawPathStart(self.resource)
        return self

    def point(self,x,y):
        """Draws a point at given ``x`` and ``y``

        :param x: :class:`~numbers.Real` x of point
        :type x: :class:`~numbers.Real`
        :param y: :class:`~numbers.Real` y of point
        :type y: :class:`~numbers.Real`

        .. versionadded:: 0.4.0
        """
        library.DrawPoint(self.resource,
                          float(x),
                          float(y))

    def rectangle(self, left=None, top=None, right=None, bottom=None,
                  width=None, height=None):
        """Draws a rectangle using the current :attr:`stoke_color`,
        :attr:`stroke_width`, and :attr:`fill_color`.

        .. sourcecode:: text

           +--------------------------------------------------+
           |              ^                         ^         |
           |              |                         |         |
           |             top                        |         |
           |              |                         |         |
           |              v                         |         |
           | <-- left --> +-------------------+  bottom       |
           |              |             ^     |     |         |
           |              | <-- width --|---> |     |         |
           |              |           height  |     |         |
           |              |             |     |     |         |
           |              |             v     |     |         |
           |              +-------------------+     v         |
           | <--------------- right ---------->               |
           +--------------------------------------------------+

        :param left: x-offset of the rectangle to draw
        :type left: :class:`numbers.Real`
        :param top: y-offset of the rectangle to draw
        :type top: :class:`numbers.Real`
        :param right: second x-offset of the rectangle to draw.
                      this parameter and ``width`` parameter are exclusive
                      each other
        :type right: :class:`numbers.Real`
        :param bottom: second y-offset of the rectangle to draw.
                       this parameter and ``height`` parameter are exclusive
                       each other
        :type bottom: :class:`numbers.Real`
        :param width: the :attr:`width` of the rectangle to draw.
                      this parameter and ``right`` parameter are exclusive
                      each other
        :type width: :class:`numbers.Real`
        :param height: the :attr:`height` of the rectangle to draw.
                       this parameter and ``bottom`` parameter are exclusive
                       each other
        :type height: :class:`numbers.Real`

        .. versionadded:: 0.3.6

        """
        if left is None:
            raise TypeError('left is missing')
        elif top is None:
            raise TypeError('top is missing')
        elif right is None and width is None:
            raise TypeError('right/width is missing')
        elif bottom is None and height is None:
            raise TypeError('bottom/height is missing')
        elif not (right is None or width is None):
            raise TypeError('parameters right and width are exclusive each '
                            'other; use one at a time')
        elif not (bottom is None or height is None):
            raise TypeError('parameters bottom and height are exclusive each '
                            'other; use one at a time')
        elif not isinstance(left, numbers.Real):
            raise TypeError('left must be numbers.Real, not ' + repr(left))
        elif not isinstance(top, numbers.Real):
            raise TypeError('top must be numbers.Real, not ' + repr(top))
        elif not (right is None or isinstance(right, numbers.Real)):
            raise TypeError('right must be numbers.Real, not ' + repr(right))
        elif not (bottom is None or isinstance(bottom , numbers.Real)):
            raise TypeError('bottom must be numbers.Real, not ' + repr(bottom))
        elif not (width is None or isinstance(width, numbers.Real)):
            raise TypeError('width must be numbers.Real, not ' + repr(width))
        elif not (height is None or isinstance(height, numbers.Real)):
            raise TypeError('height must be numbers.Real, not ' + repr(height))
        if right is None:
            if width < 0:
                raise ValueError('width must be positive, not ' + repr(width))
            right = left + width
        elif right < left:
            raise ValueError('right must be more than left ({0!r}), '
                             'not {1!r})'.format(left, right))
        if bottom is None:
            if height < 0:
                raise ValueError('height must be positive, not ' + repr(height))
            bottom = top + height
        elif bottom < top:
            raise ValueError('bottom must be more than top ({0!r}), '
                             'not {1!r})'.format(top, bottom))
        library.DrawRectangle(self.resource, left, top, right, bottom)
        self.raise_exception()

    def rotate(self, degree):
        """Applies the specified rotation to the current coordinate space.

        :param degree: degree to rotate
        :type degree: :class:`~numbers.Real`
        .. versionadded:: 0.4.0
        """
        library.DrawRotate(self.resource, float(degree))

    def polygon(self, points=None):
        """Draws a polygon using the current :attr:`stoke_color`,
        :attr:`stroke_width`, and :attr:`fill_color`, using the specified
        array of coordinates.

        Example polygon on ``image`` ::

            with Drawing() as draw:
                points = [(40,10), (20,50), (90,10), (70,40)]
                draw.polygon(points)
                draw.draw(image)

        .. versionadded:: 0.4.0

        :param points: list of x,y tuples
        :type points: :class:`list`
        """

        (points_l, points_p) = _list_to_point_info(points)
        library.DrawPolygon(self.resource, points_l,
          ctypes.cast(points_p,ctypes.POINTER(PointInfo)))

    def polyline(self, points=None):
        """Draws a polyline using the current :attr:`stoke_color`,
        :attr:`stroke_width`, and :attr:`fill_color`, using the specified
        array of coordinates.

        Identical to :class:`~wand.drawing.Drawing.polygon`, but without closed
        stroke line.

        :param points: list of x,y tuples
        :type points: :class:`list`

        .. versionadded:: 0.4.0
        """

        (points_l, points_p) = _list_to_point_info(points)
        library.DrawPolyline(self.resource, points_l,
          ctypes.cast(points_p,ctypes.POINTER(PointInfo)))

    def bezier(self, points=None):
        """Draws a bezier curve through a set of points on the image, using
        the specified array of coordinates.

        At least four points should be given to complete a bezier path.
        The first & forth point being the start & end point, and the second
        & third point controlling the direction & curve.

        Example bezier on ``image`` ::

            with Drawing() as draw:
                points = [(40,10), # Start point
                          (20,50), # First control
                          (90,10), # Second control
                          (70,40)] # End point
                draw.stroke_color = Color('#000')
                draw.fill_color = Color('#fff')
                draw.bezier(points)
                draw.draw(image)

        :param points: list of x,y tuples
        :type points: :class:`list`

        .. versionadded:: 0.4.0
        """

        (points_l, points_p) = _list_to_point_info(points)
        library.DrawBezier(self.resource, points_l,
          ctypes.cast(points_p,ctypes.POINTER(PointInfo)))

    def text(self, x, y, body):
        """Writes a text ``body`` into (``x``, ``y``).

        :param x: the left offset where to start writing a text
        :type x: :class:`numbers.Integral`
        :param y: the top offset where to start writing a text
        :type y: :class:`numbers.Integral`
        :param body: the body string to write
        :type body: :class:`basestring`

        """
        if not isinstance(x, numbers.Integral) or x < 0:
            exc = ValueError if x < 0 else TypeError
            raise exc('x must be a natural number, not ' + repr(x))
        elif not isinstance(y, numbers.Integral) or y < 0:
            exc = ValueError if y < 0 else TypeError
            raise exc('y must be a natural number, not ' + repr(y))
        elif not isinstance(body, string_type):
            raise TypeError('body must be a string, not ' + repr(body))
        elif not body:
            raise ValueError('body string cannot be empty')
        if isinstance(body, text_type):
            # According to ImageMagick C API docs, we can use only UTF-8
            # at this time, so we do hardcoding here.
            # http://imagemagick.org/api/drawing-wand.php#DrawSetTextEncoding
            if not self.text_encoding:
                self.text_encoding = 'UTF-8'
            body = body.encode(self.text_encoding)
        body_p = ctypes.create_string_buffer(body)
        library.DrawAnnotation(
            self.resource, x, y,
            ctypes.cast(body_p,ctypes.POINTER(ctypes.c_ubyte))
        )

    def skew(self, x=None, y=None):
        """Skews the current coordinate system in the horizontal direction if
        ``x`` is given, and vertical direction if ``y`` is given.

        :param x: Skew horizontal direction
        :type x: :class:`~numbers.Real`
        :param y: Skew vertical direction
        :type y: :class:`~numbers.Real`

        .. versionadded:: 0.4.0
        """
        if x is not None:
            library.DrawSkewX(self.resource, float(x))
        if y is not None:
            library.DrawSkewY(self.resource, float(y))

    def translate(self, x=None, y=None):
        """Applies a translation to the current coordinate system which moves
        the coordinate system origin to the specified coordinate.

        :param x: Skew horizontal direction
        :type x: :class:`~numbers.Real`
        :param y: Skew vertical direction
        :type y: :class:`~numbers.Real`

        .. versionadded:: 0.4.0
        """
        if x is None or y is None:
            raise TypeError('Both x & y coordinates need to be defined')
        library.DrawTranslate(self.resource, float(x), float(y))

    def get_font_metrics(self, image, text, multiline=False):
        """Queries font metrics from the given ``text``.

        :param image: the image to be drawn
        :type image: :class:`~wand.image.Image`
        :param text: the text string for get font metrics.
        :type text: :class:`basestring`
        :param multiline: text is multiline or not
        :type multiline: `boolean`

        """
        if not isinstance(image, Image):
            raise TypeError('image must be a wand.image.Image instance, not '
                            + repr(image))
        if not isinstance(text, string_type):
            raise TypeError('text must be a string, not ' + repr(text))
        if multiline:
            font_metrics_f = library.MagickQueryMultilineFontMetrics
        else:
            font_metrics_f = library.MagickQueryFontMetrics
        if isinstance(text, text_type):
            if self.text_encoding:
                text = text.encode(self.text_encoding)
            else:
                text = binary(text)
        result = font_metrics_f(image.wand, self.resource, text)
        args = (result[i] for i in xrange(13))
        return FontMetrics(*args)

    def viewbox(self, left, top, right, bottom):
      """
      Viewbox sets the overall canvas size to be recorded with the drawing
      vector data. Usually this will be specified using the same size as the
      canvas image. When the vector data is saved to SVG or MVG formats, the
      viewbox is use to specify the size of the canvas image that a viewer will
      render the vector data on.

      :param left: the left most point of the viewbox.
      :type left: :class:`~numbers.Integral`
      :param top: the top most point of the viewbox.
      :type top: :class:`~numbers.Integral`
      :param right: the right most point of the viewbox.
      :type right: :class:`~numbers.Integral`
      :param bottom: the bottom most point of the viewbox.
      :type bottom: :class:`~numbers.Integral`
      """
      if not isinstance(left, numbers.Integral):
        raise TypeError('left must be an integer, not ' + repr(left))
      if not isinstance(top, numbers.Integral):
        raise TypeError('top must be an integer, not ' + repr(top))
      if not isinstance(right, numbers.Integral):
        raise TypeError('right must be an integer, not ' + repr(right))
      if not isinstance(bottom, numbers.Integral):
        raise TypeError('bottom must be an integer, not ' + repr(bottom))
      library.DrawSetViewbox(self.resource, left, top, right, bottom)

    def __call__(self, image):
        return self.draw(image)

def _list_to_point_info(points):
    """
    Helper method to convert a list of tuples to ``const * PointInfo``

    :param points: a list of tuples
    :type points: `list`
    :returns: tuple of point length and c_double array
    :rtype: `tuple`
    :raises: `TypeError`

    .. versionadded:: 0.4.0
    """
    if not isinstance(points, list):
        raise TypeError('points must be a list, not ' + repr(points))
    point_length = len(points)
    tuple_size = 2
    point_info_size = point_length * tuple_size
    # Allocate sequence of memory
    point_info = (ctypes.c_double * point_info_size)()
    for double_index in xrange(0, point_info_size):
        tuple_index = double_index // tuple_size
        tuple_offset = double_index % tuple_size
        point_info[double_index] = ctypes.c_double(points[tuple_index][tuple_offset])
    return (point_length, point_info)
