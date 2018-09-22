import sys
import os

from PIL import Image

from karizer.CharDict import CharDict
from karizer.ConversionTable import ConversionTable
from karizer.CharImage import CharImage


if __name__ == '__main__':
    if not os.path.isdir('cache'):
        os.makedirs('cache', mode=0o744)

    print("start generating char_dict")
    char_dict = CharDict()
    char_dict.write()

    print("start generating conversion_table")
    conversion_table = ConversionTable(char_dict)
    conversion_table.write()

    if len(sys.argv) > 1:
        infile_path = sys.argv[1]
    else:
        infile_path = 'sample/sample.jpg'
    image = Image.open(infile_path)

    print("start generating char_image")
    char_image = CharImage(image, conversion_table)
    char_image.write()
