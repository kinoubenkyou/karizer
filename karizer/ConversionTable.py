class ConversionTable:

    @staticmethod
    def find_char(x, y, values):
        most_similar_char = " "
        least_difference = 255 * 255 * 2

        for char in values:
            upper, lower = values[char]
            difference = (y - upper) * (y - upper) + (x - lower) * (x - lower)
            if difference < least_difference:
                most_similar_char = char
                least_difference = difference

        return most_similar_char

    def __init__(self, char_dict):
        chars = []

        # The outer array is the upper value while
        # the inner array is the lower value of a character.
        for y in range(256):
            chars.append([])
            for x in range(256):
                chars[y].append(self.find_char(x, y, char_dict.values))

        self.chars = chars
        self.write()

    def write(self, file_path='cache/last-conversion-table'):
        with open(file_path, 'w') as file:
            for y in range(256):
                line = ''.join(self.chars[y]) + '\n'
                file.write(line)
