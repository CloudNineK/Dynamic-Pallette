""" Subdivide a Pillow Image object"""

from PIL import Image


def subdivide(image):
    """ Subdivide an image object based on its resolution
        Returns a list of cropped image objects and a tuple of the vertices
    """

    # tuple holding image size
    x, y = image.size

    # Estimate how many subdivisions to use
    x_Sub = x // 40
    y_Sub = y // 40

    # Create 2 lists holding x and y values for points at
    # subdivisions
    x_Splits = [0]
    y_Splits = [0]

    for k in range(1, 40):
        x_Splits.append(x_Splits[k - 1] + x_Sub)

    for k in range(1, 40):
        y_Splits.append(y_Splits[k - 1] + y_Sub)

    subdivisions = []
    subVAL = []

    for kx in range(len(x_Splits)):
        for ky in range(len(y_Splits)):
            # x-values
            xUL = 0 + x_Splits[kx]
            xLR = xUL + (x_Splits[1] - x_Splits[0])
            # y - values
            yUL = 0 + y_Splits[ky]
            yLR = yUL + (y_Splits[1] - y_Splits[0])

            sub = (xUL, yUL, xLR, yLR)
            subVAL.append(sub)
            subdivisions.append(image.crop(sub))

    return subdivisions

if __name__ == '__main__':
    im = Image.open('temp.jpg')
    subdivide(im)
