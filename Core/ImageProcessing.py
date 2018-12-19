
from PIL import Image as PILImage
from PIL import ImageStat as PILImageStat
from PIL import ImageEnhance as PILImageEnhance
from PIL import ImageOps as PILImageOps
from colormap import rgb2hex
import math
import os


class ImageFormats(object):
    TIF     = "tif"
    TIFF    = "tiff"
    TGA     = "TGA"
    JPG     = "jpg"
    PNG     = "png"
    JPEG    = "jpeg"


class ColorModes(object):
    MONO    = "1"       # 1-bit pixels, black and white, stored with one pixel per byte
    L       = "L"       # 8-bit pixels, black and white
    RGB     = "RGB"     # 3x8-bit pixels, true color
    RGBA    = "RGBA"    # 4x8-bit pixels, true color with transparency mask
    CMYK    = "CMYK"    # 4x8-bit pixels, color separation
    YCbCr   = "YCbCr"   # 3x8-bit pixels, color video format
    LAB     = "LAB"     # 3x8-bit pixels, the L*a*b color space
    HSV     = "HSV"     # 3x8-bit pixels, Hue, Saturation, Value color space
    I       = "I"       # 32-bit signed integer pixels
    F       = "F"       # 32-bit floating point pixels



class ImageProcessor(object):

    def __init__(self):
        super(ImageProcessor, self).__init__()

        self._image = None
        self._imageFile = ""
        self._supportedFormats = [
            ImageFormats.TIFF,
            ImageFormats.JPEG,
            ImageFormats.TIF,
            ImageFormats.TGA,
            ImageFormats.JPG,
            ImageFormats.PNG
        ]

    @property
    def imageFile(self):
        return self._imageFile

    @imageFile.setter
    def imageFile(self, imageFile):
        if not isinstance(imageFile, str):
            raise TypeError("Expected < str >")

        if not os.path.isfile(imageFile):
            raise StandardError(imageFile + " is not file")

        extension = os.path.splitext(imageFile)[-1][1:]

        if extension not in self._supportedFormats:
            raise StandardError("Unsupportable image extension")

        self._imageFile = imageFile


    def open(self):
        self._image = PILImage.open(self._imageFile)


    def close(self):
        if self._image:
            self._image.close()
            self._image = None


    def width(self):
        return self._image.width


    def height(self):
        return self._image.height


    def mode(self):
        return self._image.mode


    def desaturate(self):
        self._image = PILImageOps.grayscale(self._image)


    def invert(self):
        self._image = PILImageOps.invert(self._image)


    def changeSaturation(self, scale=1.0):
        enhancer = PILImageEnhance.Color(self._image)
        self._image = enhancer.enhance(scale)


    def changeBrightness(self, scale=1.0):
        enhancer = PILImageEnhance.Brightness(self._image)
        self._image = enhancer.enhance(scale)


    def changeContrast(self, scale=1.0):
        enhancer = PILImageEnhance.Contrast(self._image)
        self._image = enhancer.enhance(scale)


    def changeSharpness(self, scale=1.0):
        enhancer = PILImageEnhance.Sharpness(self._image)
        self._image = enhancer.enhance(scale)


    def convertTo(self, colorMode=ColorModes.RGB):
        self._image = self._image.convert(colorMode)


    def resize(self, width, height):
        self._image.thumbnail((width, height), PILImage.ANTIALIAS)


    def scale(self, width=0.5, height=0.5):
        w = self._image.width
        h = self._image.height

        w = math.ceil(w * width)
        h = math.ceil(h * height)

        self._image.thumbnail((w, h), PILImage.ANTIALIAS)


    def averageColor(self, hexType=True):
        color = PILImageStat.Stat(self._image).mean
        if hexType:
            color = rgb2hex(color[0], color[1], color[2])
        return color


    def minMax(self):
        extrema = PILImageStat.Stat(self._image).extrema
        return {
            "r": {"min": extrema[0][0], "max": extrema[0][1]},
            "g": {"min": extrema[1][0], "max": extrema[1][1]},
            "b": {"min": extrema[2][0], "max": extrema[2][1]},
        }


    def save(self, directory, name, format=ImageFormats.JPEG, compress=True, quality=100):
        path = os.path.join(directory, name + "." + format)
        self._image.save(path, format, optimize=compress, quality=quality)



if __name__ == '__main__':
    srcdir = "C:/Users/edward/Desktop/imgtest"
    dstdir = "C:/Users/edward/Desktop/imgtest"

    albedo = os.path.join(srcdir, "Albedo.png")

    manager = ImageProcessor()
    manager.imageFile = albedo
    manager.open()
    print manager.averageColor()
    #manager.save(dstdir, "processed", format=ImageFormats.JPEG)
    manager.close()

