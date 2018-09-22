import string

from PIL import Image, ImageDraw, ImageFont


class CharDict:
    # Each font has its own rule of rendering. Each size also has
    # its own rule of rendering. Therefore, the formula to calculate CharDict
    # can only be hard-coded for each set of font_name, font_size.
    FONT_FILE_NAME = 'cour.ttf'
    FONT_SIZE = 28

    CHAR_WIDTH = 16
    CHAR_HEIGHT = 32

    # The order before joining of CHAR_STRING is also the priority order
    # for choosing character when generating the conversion table.
    CHAR_STRING = ''.join([string.punctuation,
                           " ",
                           string.ascii_lowercase,
                           string.digits,
                           string.ascii_uppercase])

    def __init__(self, font_file_name=FONT_FILE_NAME, font_size=FONT_SIZE):
        values = {}

        for char in self.CHAR_STRING:
            image = Image.new('L', (self.CHAR_WIDTH, self.CHAR_HEIGHT),
                              color=255)
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('fonts/' + font_file_name, font_size)
            top_left_pos = (0, 0)
            draw.multiline_text(top_left_pos, text=char, font=font)
            half_n_pixel = self.CHAR_WIDTH * self.CHAR_HEIGHT // 2

            upper, lower = 0, 0
            for x in range(self.CHAR_WIDTH):
                # process 1 upper and 1 lower pixel for each iteration
                for y in range(self.CHAR_HEIGHT // 2):
                    # process the upper pixel
                    upper_position = (x, y)
                    upper += image.getpixel(upper_position)
                    # process the lower pixel
                    lower_position = (x, y + self.CHAR_HEIGHT // 2)
                    lower += image.getpixel(lower_position)

            upper = round(upper / half_n_pixel)
            lower = round(lower / half_n_pixel)

            values[char] = (upper, lower)
            del image

        self.values = values

    # for debugging
    def print_same_keys_of_same_values(self):
        keys = self.values.keys
        for i, lkey in enumerate(keys):
            for rkey in keys[i:]:
                lvalue = self.values[lkey]
                rvalue = self.values[rkey]
                if lvalue == rvalue:
                    print(lkey, rkey, self.values[lkey])

    def write(self, file_path='cache/last-char-dict'):
        with open(file_path, 'w') as file:
            for char in self.values:
                line_data = [char, str(self.values[char][0]),
                             str(self.values[char][1]), '\n']
                file.write(' '.join(line_data))
