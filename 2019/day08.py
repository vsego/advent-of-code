#!/usr/bin/python3

import textwrap

from PIL import Image, ImageDraw


def str2image(s, width, height):
    """
    Return image from string and dimensions.

    :param s: The string from which to create the image.
    :param width, height: Width and height of the image.
    :return: An image (a list of layers, each being a list of lists of `int`
        digits).
    """
    layer_size = width * height
    return [
        [
            [int(point) for point in line]
            for line in textwrap.wrap(layer_str, width)
        ]
        for layer_str in textwrap.wrap(s, layer_size)
    ]


def read_input(fname="day08.in", width=25, height=6):
    """
    Read the input file and return the list of numbers that it contains.

    :param fname: A string name of the file to read.
    :return: An image (a list of layers, each being a list of lists of `int`
        digits).
    """
    with open(fname) as f:
        return str2image(f.read().strip(), width, height)


def count_points(layer, value):
    """
    Return the number of points in `layer` that have value `value`.
    """
    return sum(1 for line in layer for point in line if point == value)


def fewest_digits_layer(image, value):
    """
    Return the layer with the fewest points with value `value`.
    """
    return min(image, key=lambda layer: count_points(layer, value))


def part1(image):
    """
    Return the checksum for the image.
    """
    layer = fewest_digits_layer(image, 0)
    return count_points(layer, 1) * count_points(layer, 2)


def _pixel_color(image, x, y):
    """
    Return the color of pixel `(x, y)` in the decoded version of `image`.
    """
    try:
        return next(
            point
            for point in (layer[y][x] for layer in image)
            if point != 2
        )
    except StopIteration:
        return 2


def decode_image(image):
    """
    Return decoded image.
    """
    return [
        [_pixel_color(image, x, y) for x in range(len(image[0][0]))]
        for y in range(len(image[0]))
    ]


def image_to_ascii(image, indent="  "):
    """
    Decode the image and return it as a printable string.
    """
    point2char = {0: " ", 1: "\u2588"}
    return "\n".join(
        f"{indent}{''.join(point2char[point] for point in line)}"
        for line in decode_image(image)
    )


def image_show(image, zoom=17):
    """
    Decode the image, draw it, and show it in a new window.
    """
    point2color = {0: "#000", 1: "#fff"}
    decoded = decode_image(image)
    dims = (len(decoded[0]), len(decoded))
    size = tuple(zoom * v for v in dims)
    pil_image = Image.new("RGB", size, "#ff0000")
    d = ImageDraw.Draw(pil_image)
    for y, line in enumerate(decode_image(image)):
        for x, point in enumerate(line):
            d.rectangle(
                (x * zoom, y * zoom, (x + 1) * zoom - 1, (y + 1) * zoom - 1),
                fill=point2color[point],
            )
    pil_image.show()


def part2(image, indent="  "):
    """
    Decode the image and show it in a new window and printed to the console.
    """
    image_show(image)
    return image_to_ascii(image, indent)


def test_decoding():
    """
    Test image decoding.
    """
    print("Testing image decoding...", end="")
    correct = [[0, 1], [1, 0]]
    image = str2image("0222112222120000", 2, 2)
    result = decode_image(image)
    if result == correct:
        print(" OK!")
    else:
        print(f"Failed: {result} != {correct}")


if __name__ == "__main__":
    image = read_input()
    test_decoding()
    print("Part 1:", part1(image))
    print("Part 2:")
    print(part2(image))
