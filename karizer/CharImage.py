from PIL import Image, ImageStat


class CharImage:

    @staticmethod
    def prepare_image(image, char_image_width, resampler='bilinear'):
        image_width, image_height = image.size
        char_image_height = round(char_image_width * image_height
                                  / image_width // 2)

        if resampler == 'lanczos':
            resample_filter = Image.LANCZOS
        elif resampler == 'bicubic':
            resample_filter = Image.BICUBIC
        else:
            resample_filter = Image.BILINEAR

        resized_size = (char_image_width, char_image_height * 2)
        resized_image = image.resize(resized_size, resample_filter)
        resized_image.save('cache/last-resized-image.png')

        converted_image = resized_image.convert(mode='L')
        converted_image.save('cache/last-converted-image.png')
        return converted_image, char_image_width, char_image_height

    @staticmethod
    def adjust_value(value, stat):
        mean = stat.mean[0]
        # hard-coded for sample image
        adjusted_mean = 255 * (1 - (1 / 2 ** 5))

        if value > mean:
            value = round(255 - (255 - value) *
                          (255 - adjusted_mean) / (255 - mean))
        else:
            value = round(value * adjusted_mean / mean)

        return value

    def __init__(self, image, conversion_table, char_image_width=300):
        preparing_result = self.prepare_image(image,
                                              char_image_width)
        prepared_image, char_image_width, char_image_height = preparing_result
        stat = ImageStat.Stat(prepared_image)

        chars = []
        for y in range(char_image_height):
            row = []
            for x in range(char_image_width):
                position = (x, y * 2)
                upper = prepared_image.getpixel(position)
                upper = self.adjust_value(upper, stat)

                position = (x, y * 2 + 1)
                lower = prepared_image.getpixel(position)
                lower = self.adjust_value(lower, stat)

                row.append(conversion_table.chars[upper][lower])

            chars.append(row)

        self.chars = chars
        self.write()

    def write(self, file_path='cache/last-char-image'):
        with open(file_path, 'w') as file:
            for y in range(len(self.chars)):
                line = ''.join(self.chars[y]) + '\n'
                file.write(line)
