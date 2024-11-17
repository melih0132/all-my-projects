import requests
import os
from datetime import datetime
import ctypes

# 1. Récupérer la météo via wttr.in (pas besoin de clé API)
city = "Annecy"
url = f'http://wttr.in/{city}?format=%C'
weather = requests.get(url).text.strip()

# Vérifier la météo récupérée
print(f"Météo actuelle à {city} : {weather}")

# 2. Obtenir l'heure actuelle
current_hour = datetime.now().hour

# Vérifier l'heure récupérée
print(f"Heure actuelle : {current_hour}")

# 3. Choisir le fond d'écran en fonction de la météo et de l'heure
if weather == 'Clear' and current_hour < 18:
    wallpaper = r"C:\Users\melih\Pictures\WallPaper\2\RUE\4.jpg"
elif weather == 'Rain' and current_hour > 18:
    wallpaper = r"C:\Users\melih\Pictures\WallPaper\2\RUE\6.jpg"
elif weather == 'Clear' and current_hour > 18 and current_hour < 22:
    wallpaper = r"C:\Users\melih\Pictures\WallPaper\2\RUE\3.jpg"
else:
    wallpaper = r"C:\Users\melih\Pictures\WallPaper\2\RUE\2.jpg"

# Vérifier si le fichier existe
if os.path.exists(wallpaper):
    print(f"Le fond d'écran sélectionné est : {wallpaper}")
else:
    print(f"Le fichier {wallpaper} n'existe pas, vérifiez le chemin.")

# 4. Changer le fond d'écran sous Windows
ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper, 0)