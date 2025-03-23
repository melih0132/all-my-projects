

from PIL import Image
import numpy as np

def convertImageToAscii(imageFilename, txtFilename, blocSize, mode="txt"):
	image = np.asarray(Image.open(imageFilename), dtype='int32')

	h = len(image)
	w = len(image[0])
	R = 0
	G = 1
	B = 2

	blocW = blocSize
	blocH = int(h*blocW/w)

	nbBlocHorizontal = int(w/blocW)
	nbBlocVertical = h//blocH

	pixelsPerChar = [  (32,0)    ,(33,37),(34,51),(35,98),(36,87),(37,88),(38,71),(39,25),(40,42),(41,48),(42,44),(43,46),(44,26),(45,24),(46,15),(47,44),(48,80),(49,49),(50,72),(51,69),(52,71),(53,74),(54,84),(55,50),(56,93),(57,83),(58,30),(59,44),(60,50),(61,39),(62,52),(63,56),(64,98),(65,83),(66,92),(67,71),(68,78),(69,87),(70,77),(71,83),(72,85),(73,52),(74,62),(75,94),(76,55),(77,105),(78,100),(79,82),(80,73),(81,102),(82,88),(83,86),(84,62),(85,82),(86,74),(87,109),(88,88),(89,67),(90,74),(91,47),(92,43),(93,47),(94,32),(95,28),(96,15),(97,78),(98,88),(99,66),(100,91),(101,82),(102,62),(103,81),(104,72),(105,42),(106,51),(107,77),(108,45),(109,87),(110,60),(111,67),(112,80),(113,85),(114,50),(115,70),(116,58),(117,64),(118,61),(119,78),(120,75),(121,65),(122,61),(123,49),(124,36),(125,48),(126,28),]
	pixelsPerChar.sort(key=lambda y: y[1])
	maxPixelsPerChar = 109

	# brightness entre 0 et 255
	def characterForBrightness(brightness): 
		nbPotentialPixels = maxPixelsPerChar - maxPixelsPerChar * brightness/255
		idealAscii = 32
		i = 0
		found = False
		while i<len(pixelsPerChar) and not found:
			asciiCode, nbPixels = pixelsPerChar[i]
			found = nbPixels > nbPotentialPixels
			idealAscii = asciiCode
			i += 1

		return chr(idealAscii)



	ascii = ""
	if mode=="html":
		ascii = "<style>span { font-family: monospace; }</style>"

	for indexBlocVertical in range(nbBlocVertical):
		for indexBlocHorizontal in range(nbBlocHorizontal):
			# Coordonées X y du bloc dans l'image 
			xBloc = indexBlocHorizontal*blocW
			yBloc = indexBlocVertical*blocH
			# Luminosité : entre 0 (noir) et 255 (blanc)
			# Parcourir les pixels de chaque bloc
			sum = 0
			for y in range(yBloc, yBloc+blocH):
				for x in range(xBloc, xBloc+blocW):
					sum +=  (image[y][x][R] + \
						     image[y][x][G] + \
						     image[y][x][B])/3
			brightness = sum/(blocH*blocW)
			# Choix du caractère en fonction de la luminosité
			char = characterForBrightness(brightness)

			if mode == "html":
				ascii += "<span style='background-color: rgb("+str(brightness)+ \
					","+str(brightness)+","+str(brightness)+");'>"
			ascii += char
			# ascii += "&nbsp;"
			if mode == "html":
				ascii += "</span>"


		ascii += "\n"
		if mode == "html":
			ascii += "<br/>"


	f = open(txtFilename, "w")
	a = f.write(ascii)
	f.close()


convertImageToAscii("ethann.jpg", "ethann.html", 3, "html")
# convertImageToAscii("mohamed.jpg", "mohamed.html", 10, "html")
# convertImageToAscii("worm.jpg", "worm.txt", 3, "txt")



