# Try to import PIL in either of the two ways it can be installed.
try:
    from PIL import Image, ImageDraw
except ImportError:
    try:
        import Image, ImageDraw
    except ImportError:
        Image = None
        ImageDraw = None


class BaseImage(object):
    def __init__(self, border, width, box_size):
        self.kind = None
        self.border = border
        self.width = width
        self.box_size = box_size

    def drawrect(self, row, col):
        raise NotImplementedError("BaseImage.drawrect")

    def save(self, stream, kind=None):
        raise NotImplementedError("BaseImage.save")


class PngImage(BaseImage):
    """PIL image builder, default format is PNG."""

    def __init__(self, border, width, box_size):
        if Image is None and ImageDraw is None:
            raise NotImplementedError("PIL not available")
        super(PngImage, self).__init__(border, width, box_size)
        self.kind = "PNG"

        pixelsize = (self.width + self.border * 2) * self.box_size
        self._img = Image.new("1", (pixelsize, pixelsize), "white")
        self._idr = ImageDraw.Draw(self._img)

    def drawrect(self, row, col):
        x = (col + self.border) * self.box_size
        y = (row + self.border) * self.box_size
        box = [(x, y),
               (x + self.box_size - 1,
                y + self.box_size - 1)]
        self._idr.rectangle(box, fill="black")

    def save(self, stream, kind=None):
        if kind is None:
            kind = self.kind
        self._img.save(stream, kind)
