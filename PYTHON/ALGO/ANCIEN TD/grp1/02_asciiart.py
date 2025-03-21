from PIL import Image
import numpy as np


def imageToAscii(inFilename, outFilename, outType):

	#---LOAD
	image = np.asarray(Image.open(inFilename), dtype='int32')

	h = len(image)
	w = len(image[0])


	#---CONFIG
	blocW = 5   # à régler en fonction
	blocH = 7   # de la taille de l'image

	R = 0
	G = 1
	B = 2

	nbBlocsY = int(h/blocH)
	nbBlocsX = int(w/blocW)

	#---BRIGHTNESS

	pixelsPerChar = [(32,0),(33,37),(34,51),(35,98),(36,87),(37,88),(38,71),(39,25),(40,42),(41,48),(42,44),(43,46),(44,26),(45,24),(46,15),(47,44),(48,80),(49,49),(50,72),(51,69),(52,71),(53,74),(54,84),(55,50),(56,93),(57,83),(58,30),(59,44),(60,50),(61,39),(62,52),(63,56),(64,98),(65,83),(66,92),(67,71),(68,78),(69,87),(70,77),(71,83),(72,85),(73,52),(74,62),(75,94),(76,55),(77,105),(78,100),(79,82),(80,73),(81,102),(82,88),(83,86),(84,62),(85,82),(86,74),(87,109),(88,88),(89,67),(90,74),(91,47),(92,43),(93,47),(94,32),(95,28),(96,15),(97,78),(98,88),(99,66),(100,91),(101,82),(102,62),(103,81),(104,72),(105,42),(106,51),(107,77),(108,45),(109,87),(110,60),(111,67),(112,80),(113,85),(114,50),(115,70),(116,58),(117,64),(118,61),(119,78),(120,75),(121,65),(122,61),(123,49),(124,36),(125,48),(126,28)]
	pixelsPerChar.sort(key=lambda y: y[1])
	maxPixelsPerChar = 109

	def out(char, outType, color):
		if char == "\n" and outType == "html":
			return "<br/>"
		elif char == " " and outType == "html":
			return "<span>&nbsp;</span>"
		else:
			s = ""
			if outType == "html":
				r = color[R]
				g = color[G]
				b = color[B]
				s += "<span style='background-color: rgb("+str(r)+","+str(g)+","+str(b)+"); color: rgba("+str(255-r)+","+str(255-g)+","+str(255-b)+",0.3);'>"
			s += char
			if outType == "html":
				s += "</span>"

			return s


	def characterForBrightness(brightness, color):
		idealNbPixel =  int(maxPixelsPerChar * (1 - brightness/255))

		min = maxPixelsPerChar
		selectedAscii = 32
		for ascii,nbPixels in pixelsPerChar:
			diff = abs(idealNbPixel - nbPixels)
			if diff < min:
				min = diff
				selectedAscii = ascii
		return out(chr(selectedAscii), outType, color)

	#---GENERATE ASCII	
	ascii = ""
	if outType == "html":
		ascii += "<style>span { font-family: monospace; }</style>"

	for indexBlocY in range(nbBlocsY):
		for indexBlocX in range(nbBlocsX):
			# coordonnée du bloc dans l'image
			imageBlocY = indexBlocY*blocH
			imageBlocX = indexBlocX*blocW
			pixel = image[imageBlocY][imageBlocX]
			brightness = (pixel[R]+pixel[G]+pixel[B])/3
			ascii += characterForBrightness(brightness, pixel)

		ascii += out("\n",outType, [0,0,0])


	f = open(outFilename, "w")
	a = f.write(ascii)
	f.close()


imageToAscii("worm.jpg","worm.html", "html")
# imageToAscii("amodon.jpg","amodon.html", "html")
# imageToAscii("amodon.jpg","amodon.txt", "text")
# imageToAscii("marouane.jpg","marouane.html","html")
