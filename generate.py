#!/usr/bin/python3.5

import sys
import math
from Subdivide import subdivide
from PIL import Image, ImageDraw
from numpy import arange


def main():
    """ Output GIF image with Dynamic Palette from GIF Image"""

    # Open GIF
    fName = sys.argv[1]
    outName = sys.argv[2]
    im = Image.open(fName)

    # Create palette frames and append to list
    frames = []
    try:
        frames.append(createFrame(im))
        while True:
            im.seek(im.tell() + 1)
            frames.append(createFrame(im))
    except EOFError:
        pass

    frames[0].save(outName, save_all=True, append_images=frames[1:], loop=0,
                   duration=im.info['duration'])


def createFrame(image):
    img = image.convert('RGB')

    # Subdivide the image into sections
    subs = subdivide(img)

    # Get the average color of each subsection
    averages = []
    for sub in subs:
        r, g, b = 0, 0, 0
        n = len(sub.getcolors())

        for col in sub.getcolors():
            r += col[1][0]
            g += col[1][1]
            b += col[1][2]

        averages.append(((r // n), (g // n), (b // n)))

    # Alan Zucconi Lumonosity Color Sort
    # Sort subdivisions based on luminosity
    def lum(r, g, b):
        return math.sqrt((.241 * r) + (.691 * g) + (.068 * b))
    averages.sort(key=lambda rgb: lum(*rgb))

    # Create 8 palette squares to display
    # Must have at least 8 colors FIX THIS
    palette = []
    step = len(averages) // 8
    for k in arange(0, len(averages), step)[1:9]:
        palette.append(averages[k])

    # Draw new image by pasting palette and original image onto canvas
    x, y = image.size
    a = y // 8
    b = y // 8

    nIM = Image.new('RGBA', (x + (2 * a), y + (3 * a)),
                    color=(246, 240, 236, 0))
    nIM.paste(image, (a, a, a + x, a + y))

    draw = ImageDraw.Draw(nIM)

    vert = (y + (2 * b)) - (a + y)
    x0 = a
    y0 = y + vert + (0.5 * a)
    y1 = y0 + (0.5 * a)
    iter = x // len(palette)

    for k in range(len(palette)):
        draw.rectangle([x0, y0, x0 + iter, y1], palette[k])
        x0 += iter

    del draw
    return nIM

if __name__ == "__main__":
    main()
