from array import *


class Tool(object):
    @classmethod
    def convert(cls, image):
        data_image = array('B')
        pixel = image.load()
        width, height = image.size
        for x in range(0, width):
            for y in range(0, height):
                data_image.append(pixel[y, x])

        return data_image
