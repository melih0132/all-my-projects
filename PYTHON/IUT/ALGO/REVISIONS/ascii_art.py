from PIL import Image
import numpy as np

def imageToAscii(inFilename, outFilename):
    """ Convertit une image en ASCII art. """
    image = np.asarray(Image.open(inFilename), dtype='int32')

    R, G, B = 0, 1, 2

    nbBlocHorizontal, nbBlocVertical = 200, 200
    w, h = image.shape[1], image.shape[0]
    blocWidth, blocHeight = w // nbBlocHorizontal, h // nbBlocVertical

    pixelsPerChar = [
        (32, 0), (35, 98), (36, 87), (64, 98), (65, 83), (88, 88), (90, 74), (126, 28)
    ]
    
    pixelsPerChar.sort(key=lambda y: y[1])
    maxPixelsPerChar = 109

    def characterBrightness(brightness):
        nbPixelsIdeal = maxPixelsPerChar - maxPixelsPerChar * brightness / 255
        for asciiCode, nbPixels in pixelsPerChar:
            if nbPixels > nbPixelsIdeal:
                return chr(asciiCode)
        return ' '

    asciiImage = ""
    for y in range(nbBlocVertical):
        for x in range(nbBlocHorizontal):
            blocX, blocY = int(w * x / nbBlocHorizontal), int(h * y / nbBlocVertical)
            sumBrightness = sum(
                (image[i][j][R] + image[i][j][G] + image[i][j][B]) // 3
                for i in range(blocY, min(blocY + blocHeight, h))
                for j in range(blocX, min(blocX + blocWidth, w))
            )
            brightness = sumBrightness / (blocWidth * blocHeight)
            asciiImage += characterBrightness(brightness)
        asciiImage += "\n"

    with open(outFilename, 'w') as f:
        f.write(asciiImage)

imageToAscii("image.jpg", "output.txt")
