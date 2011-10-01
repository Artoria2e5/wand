import os.path
import tempfile
from attest import  Tests, raises
from wand.image import Image, ClosedImageError


tests = Tests()


def asset(filename):
    return os.path.join(os.path.dirname(__file__), 'assets', filename)


@tests.test
def new_from_filename():
    """Opens an image through its filename."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        assert img.width == 402
    with raises(ClosedImageError):
        img.wand


@tests.test
def clone():
    """Cloens the existing image."""
    funcs = (lambda img: Image(image=img),
             lambda img: img.clone())
    with Image(filename=asset('mona-lisa.jpg')) as img:
        for func in funcs:
            with func(img) as cloned:
                assert img.wand is not cloned.wand
                assert img.size == cloned.size
            with raises(ClosedImageError):
                cloned.wand
    with raises(ClosedImageError):
        img.wand


@tests.test
def save():
    """Saves an image."""
    savefile = os.path.join(tempfile.mkdtemp(), 'savetest.jpg')
    with Image(filename=asset('mona-lisa.jpg')) as orig:
        orig.save(savefile)
    assert os.path.isfile(savefile)
    with Image(filename=savefile) as saved:
        assert saved.size == (402, 599)
    os.remove(savefile)


@tests.test
def size():
    """Gets the image size."""
    with Image(filename=asset('mona-lisa.jpg')) as img:
        assert img.size == (402, 599)
        assert img.width == 402
        assert img.height == 599

