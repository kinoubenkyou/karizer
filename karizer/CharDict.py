import string

from PIL import Image, ImageDraw, ImageFont


class CharDict:
    # Each font has its own rule of rendering. Each size also has
    # its own rule of rendering. Therefore, the formula to calculate CharDict
    # can only be hard-coded for each set of font_name, font_size.
    FONT_FILE_NAME = 'cour.ttf'
    FONT_SIZE = 14
    SPACING = 5
    RENDER_OFFSET = -1

    # The order before joining of CHAR_STRING is also the priority order
    # for choosing character when generating the conversion table.
    CHAR_STRING = ''.join([string.punctuation,
                           " ",
                           string.ascii_lowercase,
                           string.digits,
                           string.ascii_uppercase])

    @staticmethod
    def get_char_size(font_file_name, font_size, spacing):
        image = Image.new('L', size=(0, 0), color=255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('fonts/' + font_file_name, font_size)
        # dummy text is used here to get character size
        return draw.multiline_textsize(' ', font, spacing)

    def __init__(self, font_file_name=FONT_FILE_NAME, font_size=FONT_SIZE,
                 spacing=SPACING):
        values = {}
        char_width, char_height = self.get_char_size(font_file_name)

        for char in self.CHAR_STRING:
            image = Image.new('L', (char_width * 3, char_height * 3),
                              color=255)
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('fonts/' + font_file_name, font_size)
            text = '\n ' + char
            top_left_pos = (0, 0)
            draw.multiline_text(top_left_pos, text, font)
            half_n_pixel = char_width * char_height

            upper, lower = 0, 0
            for x in range(char_width, char_width * 2):
                # process 1 upper and 1 lower pixel for each iteration
                for y in range(char_height + self.RENDER_OFFSET,
                               char_height * 3 / 2 + self.RENDER_OFFSET):
                    # process the upper pixel
                    upper_position = (x, y)
                    upper += image.getpixel(upper_position)
                    # process the lower pixel
                    lower_position = (x, y + char_height / 2)
                    lower += image.getpixel(lower_position)

                upper = round(upper / half_n_pixel)
                lower = round(lower / half_n_pixel)

            values[char] = (upper, lower)
            del image

    # for debugging
    def print_same_keys_of_same_values(self):
        keys = self.values.keys
        for i, lkey in enumerate(keys):
            for rkey in keys[i:]:
                lvalue = self.values[lkey]
                rvalue = self.values[rkey]
                if lvalue == rvalue:
                    print(lkey, rkey, self.values[lkey])
