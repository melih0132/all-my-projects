from PIL import Image
import numpy as np

def imageToAscii(inFilename, outFilename):
    image = np.asarray(Image.open(inFilename), dtype='int32')

    R = 0
    G = 1
    B = 2

    nbBlocHorizontal = 200
    nbBlocVertical = 200

    w = image.shape[1]
    h = image.shape[0]

    blocHeight = h // nbBlocVertical
    blocWidth = w // nbBlocHorizontal

    pixelsPerChar = [
        (32, 0), (33, 37), (34, 51), (35, 98), (36, 87),
        (37, 88), (38, 71), (39, 25), (40, 42), (41, 48),
        (42, 44), (43, 46), (44, 26), (45, 24), (46, 15),
        (47, 44), (48, 80), (49, 49), (50, 72), (51, 69),
        (52, 71), (53, 74), (54, 84), (55, 50), (56, 93),
        (57, 83), (58, 30), (59, 44), (60, 50), (61, 39),
        (62, 52), (63, 56), (64, 98), (65, 83), (66, 92),
        (67, 71), (68, 78), (69, 87), (70, 77), (71, 83),
        (72, 85), (73, 52), (74, 62), (75, 94), (76, 55),
        (77, 105), (78, 100), (79, 82), (80, 73), (81, 102),
        (82, 88), (83, 86), (84, 62), (85, 82), (86, 74),
        (87, 109), (88, 88), (89, 67), (90, 74), (91, 47),
        (92, 43), (93, 47), (94, 32), (95, 28), (96, 15),
        (97, 78), (98, 88), (99, 66), (100, 91), (101, 82),
        (102, 62), (103, 81), (104, 72), (105, 42), (106, 51),
        (107, 77), (108, 45), (109, 87), (110, 60), (111, 67),
        (112, 80), (113, 85), (114, 50), (115, 70), (116, 58),
        (117, 64), (118, 61), (119, 78), (120, 75), (121, 65),
        (122, 61), (123, 49), (124, 36), (125, 48), (126, 28)
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

    for indexBlocVertical in range(nbBlocVertical):
        for indexBlocHorizontal in range(nbBlocHorizontal):
            blocX = int(w * indexBlocHorizontal / nbBlocHorizontal)
            blocY = int(h * indexBlocVertical / nbBlocVertical)

            sumBrightness = 0
            for y in range(blocY, min(blocY + blocHeight, h)):
                for x in range(blocX, min(blocX + blocWidth, w)):
                    sumBrightness += ((image[y][x][R] + image[y][x][G] + image[y][x][B]) // 3)
            brightness = sumBrightness / (blocWidth * blocHeight)

            asciiImage += characterBrightness(brightness)

        asciiImage += "\n"

    with open(outFilename, 'w') as f:
        f.write(asciiImage)

imageToAscii("P:\R3.02 Algo\TD\TD1\EX2\worm.jpg", "P:\R3.02 Algo\TD\TD1\worm.txt")