from PIL import Image
import numpy as np


def imageToAscii(imageFilename, textFilename):
	image = np.asarray(Image.open(imageFilename), dtype='int32')

	w = len(image[0])
	h = len(image)
	# print(w,h)

	R = 0
	G = 1
	B = 2

	# Configuration à réglages
	nbBlocHorizontal = 200
	nbBlocVertical = 200

	blocHeight = int(h/nbBlocHorizontal)
	blocWidth = int(w/nbBlocVertical)

	pixelsPerChar = [(32,0),(33,37),(34,51),(35,98),(36,87),(37,88),(38,71),(39,25),(40,42),(41,48),(42,44),(43,46),(44,26),(45,24),(46,15),(47,44),(48,80),(49,49),(50,72),(51,69),(52,71),(53,74),(54,84),(55,50),(56,93),(57,83),(58,30),(59,44),(60,50),(61,39),(62,52),(63,56),(64,98),(65,83),(66,92),(67,71),(68,78),(69,87),(70,77),(71,83),(72,85),(73,52),(74,62),(75,94),(76,55),(77,105),(78,100),(79,82),(80,73),(81,102),(82,88),(83,86),(84,62),(85,82),(86,74),(87,109),(88,88),(89,67),(90,74),(91,47),(92,43),(93,47),(94,32),(95,28),(96,15),(97,78),(98,88),(99,66),(100,91),(101,82),(102,62),(103,81),(104,72),(105,42),(106,51),(107,77),(108,45),(109,87),(110,60),(111,67),(112,80),(113,85),(114,50),(115,70),(116,58),(117,64),(118,61),(119,78),(120,75),(121,65),(122,61),(123,49),(124,36),(125,48),(126,28)]
	pixelsPerChar.sort(key=lambda y: y[1])
	maxPixelsPerChar = 109

	def charForBrightness(brightness):
		nbPixelsIdeal =  maxPixelsPerChar -  maxPixelsPerChar * brightness / 255
		i = 0
		found = False
		foundAscii = 32
		while i < len(pixelsPerChar) and not found:
			asciiCode, nbPixels = pixelsPerChar[i]
			found = nbPixels > nbPixelsIdeal
			foundAscii = asciiCode
			i += 1
		return chr(foundAscii)

	asciiImage = ""

	for indexBlocVertical in range(nbBlocVertical):
		for indexBlocHorizontal in range(nbBlocHorizontal):
			blocX = int(w * indexBlocHorizontal/nbBlocHorizontal)
			blocY = int(h * indexBlocVertical/nbBlocVertical)

			sum = 0
			for y in range(blocY, blocY+blocHeight):
				for x in range(blocX, blocX+blocWidth):
					sum += (image[y][x][R]+image[y][x][G]+image[y][x][B])/3
			brightness = sum/(blocWidth*blocHeight)

			asciiImage += charForBrightness(brightness)
		asciiImage += "\n"

	f = open(textFilename, "w")
	a = f.write(asciiImage)
	f.close()




imageToAscii("laetitia.jpg", "laetitia.txt")
imageToAscii("worm.jpg", "worm.txt")

