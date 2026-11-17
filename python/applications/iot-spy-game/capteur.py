import paho.mqtt.client as mqtt
import requests
import time
import json
import random
import sys
import threading
from collections import defaultdict
import numpy as np

# Forcer l'encodage UTF-8 pour la sortie console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


class GenerateurTemperatureEspion:
    """
    Générateur de températures aberrantes utilisant la loi normale (Gaussienne) SUBTILE.
    
    Principe :
    - Moyenne proche des capteurs normaux (camouflage)
    - Écart-type légèrement supérieur (20-40% de plus)
    - Génère des anomalies discrètes
    """

    def __init__(self, moyenne=10.0, ecart_type=3.5, min_temp=-10.0, max_temp=30.0):
        """
        Initialise le générateur avec les paramètres de la loi normale.
        
        Args:
            moyenne: Température moyenne (proche des capteurs normaux)
            ecart_type: Écart-type (légèrement supérieur aux normaux)
            min_temp: Température minimale acceptable
            max_temp: Température maximale acceptable
        """
        self.moyenne = moyenne
        self.ecart_type = ecart_type
        self.min_temp = min_temp
        self.max_temp = max_temp
        
        print(f"[ESPION] Générateur de loi normale subtile initialisé")
        print(f"[ESPION] Paramètres : μ={moyenne}°C, σ={ecart_type}°C")
        print(f"[ESPION] Plage : [{min_temp}°C, {max_temp}°C]")

    def generer_temperature_aberrante(self):
        """
        Génère une température suivant la loi normale avec clipping.
        
        Returns:
            float: Température en degrés Celsius
        """
        temperature = np.random.normal(self.moyenne, self.ecart_type)
        temperature = np.clip(temperature, self.min_temp, self.max_temp)
        return round(temperature, 1)

    def ajuster_parametres(self, moyenne_observee, ecart_type_observe):
        """
        Ajuste dynamiquement les paramètres en fonction des autres capteurs.
        
        Args:
            moyenne_observee: Moyenne des températures des autres capteurs
            ecart_type_observe: Écart-type des autres capteurs
        """
        self.moyenne = moyenne_observee + random.uniform(-0.5, 1.5)
        self.ecart_type = ecart_type_observe * random.uniform(1.3, 1.5)
        
        print(f"[ESPION] Ajustement : μ={self.moyenne:.1f}°C, σ={self.ecart_type:.1f}°C")


class AnalyseurIA:
    """
    Agent d'analyse utilisant Ollama pour détecter l'espion.
    Délègue toute la logique d'analyse au LLM.
    """

    def __init__(self, ollama_url="http://10.103.1.12:11434"):
        self.ollama_url = ollama_url
        self.modele = "gemma3:4b"
        self.timeout_requete = 60
        self.ollama_disponible = self._tester_connexion()

    def _tester_connexion(self):
        """Teste la connectivité au serveur Ollama."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print("[IA] Connexion à Ollama établie")
                return True
            return False
        except Exception as e:
            print(f"[IA] Ollama indisponible : {e}")
            return False

    def _appeler_ollama(self, prompt, timeout=60):
        """
        Appelle l'API Ollama avec gestion d'erreur.
        
        Args:
            prompt: Le prompt à envoyer au LLM
            timeout: Timeout de la requête en secondes
            
        Returns:
            str: Réponse du LLM ou None en cas d'erreur
        """
        try:
            payload = {
                "model": self.modele,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,  # Faible pour réponses déterministes
                    "top_p": 0.85,
                    "num_predict": 512
                }
            }

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=timeout
            )

            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                print(f"[IA] Erreur HTTP {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            print(f"[IA] Timeout après {timeout}s")
            return None
        except Exception as e:
            print(f"[IA] Erreur Ollama : {e}")
            return None

    def _construire_prompt_detective(self, mon_id, mes_temps, autres_temps, capteurs_ips):
        """
        Construit le prompt complet pour demander au LLM de détecter l'espion.
        
        Args:
            mon_id: Identifiant du capteur courant
            mes_temps: Liste des températures publiées par ce capteur
            autres_temps: Dictionnaire {capteur_id: [températures]}
            capteurs_ips: Dictionnaire {capteur_id: adresse_ip}
            
        Returns:
            str: Prompt formaté pour le LLM
        """
        prompt = f"""Tu es un détective spécialisé dans la détection d'anomalies dans des réseaux de capteurs IoT.

CONTEXTE DU JEU :
- 4 capteurs de température (rpi1, rpi2, rpi3, rpi4) situés dans des villes européennes PROCHES
- Villes : Annecy (rpi1), Lyon (rpi2), Grenoble (rpi3), Genève (rpi4)
- Chaque capteur publie 5 températures espacées de 5 secondes
- Un capteur est un ESPION qui publie de fausses données
- L'espion utilise une loi normale SUBTILE (μ proche du groupe, σ légèrement supérieur)

TU ES LE CAPTEUR : {mon_id}

DONNÉES À ANALYSER :

Mon capteur {mon_id} (IP: {capteurs_ips.get(mon_id, 'inconnue')})
  Températures publiées : {mes_temps}
  Moyenne : {np.mean(mes_temps):.1f}°C
  Écart-type : {np.std(mes_temps):.2f}°C

"""

        # Ajout des données des autres capteurs
        for capteur_id in sorted(autres_temps.keys()):
            temps = autres_temps[capteur_id]
            ip = capteurs_ips.get(capteur_id, 'inconnue')
            
            if len(temps) > 0:
                moyenne = np.mean(temps)
                ecart_type = np.std(temps)
                prompt += f"Capteur {capteur_id} (IP: {ip})\n"
                prompt += f"  Températures reçues : {temps}\n"
                prompt += f"  Moyenne : {moyenne:.1f}°C\n"
                prompt += f"  Écart-type : {ecart_type:.2f}°C\n\n"
            else:
                prompt += f"Capteur {capteur_id} (IP: {ip})\n"
                prompt += f"  AUCUNE DONNÉE REÇUE (TRÈS SUSPECT)\n\n"

        prompt += """
MÉTHODOLOGIE D'ANALYSE :

1. Cohérence géographique
   - Les villes sont PROCHES (rayon 150km)
   - Écart maximal attendu : 5°C
   - Si un capteur s'écarte de >5°C de la moyenne du groupe → SUSPECT

2. Stabilité temporelle
   - Températures réelles évoluent PROGRESSIVEMENT
   - Variations brusques >3°C entre mesures consécutives → SUSPECT
   - Calcul : max(|T[i+1] - T[i]|) pour i=0 à 3

3. Variabilité statistique
   - Écart-type normal attendu : 1.0-2.5°C
   - Écart-type >3.0°C → SUSPECT (loi normale artificielle)
   - Comparer l'écart-type de chaque capteur

4. Absence de données
   - Si un capteur n'a publié AUCUNE température → TRÈS SUSPECT

CALCULS REQUIS :
Pour chaque capteur :
- Moyenne des 5 températures
- Écart-type
- Variation maximale entre mesures consécutives
- Écart à la moyenne du groupe

RÈGLES DE DÉCISION :
- Écart-type >3.0°C ET (variation max >3°C OU écart au groupe >5°C) → Confiance 95%
- Écart-type >2.5°C ET écart au groupe >4°C → Confiance 80%
- Aucune donnée reçue → Confiance 99%
- Sinon → Confiance 40-60% (incertitude)

FORMAT DE SORTIE :
Tu DOIS répondre UNIQUEMENT avec un objet JSON valide (sans texte avant/après) :

{
  "suspect": "rpiX",
  "confiance": 0.85,
  "preuves": [
    "Écart-type de 4.2°C (attendu <2.5°C)",
    "Variation maximale de 5.1°C entre mesures",
    "Écart de 6.3°C par rapport à la moyenne du groupe"
  ],
  "analyse_comparative": "Le capteur rpiX présente un écart-type anormalement élevé et des variations incompatibles avec des mesures météorologiques réelles dans des villes proches."
}

IMPORTANT :
- "suspect" doit être "rpi1", "rpi2", "rpi3" ou "rpi4"
- "confiance" entre 0.0 et 1.0
- "preuves" : liste de 2-4 arguments factuels
- Pas de texte avant ou après le JSON

ANALYSE :"""

        return prompt

    def analyser_espion(self, mon_id, mes_temperatures, temperatures_autres, capteurs_ips, je_suis_espion=False):
        """
        Analyse complète pour identifier l'espion.
        
        Args:
            mon_id: Identifiant du capteur courant
            mes_temperatures: Liste des températures publiées
            temperatures_autres: Dictionnaire {capteur_id: [températures]}
            capteurs_ips: Dictionnaire {capteur_id: adresse_ip}
            je_suis_espion: Booléen indiquant si ce capteur est l'espion
            
        Returns:
            dict: Résultat de l'analyse avec format standardisé
        """
        # Cas particulier : l'espion vote au hasard
        if je_suis_espion:
            return self._vote_espion(mon_id, list(temperatures_autres.keys()))

        # Vérifier disponibilité de l'IA
        if not self.ollama_disponible:
            print(f"[{mon_id}] [IA] Ollama indisponible, vote aléatoire")
            return self._vote_aleatoire(mon_id, list(temperatures_autres.keys()))

        # Construction du prompt
        prompt = self._construire_prompt_detective(
            mon_id,
            mes_temperatures,
            temperatures_autres,
            capteurs_ips
        )

        # Appel à Ollama avec retry
        max_tentatives = 2
        for tentative in range(max_tentatives):
            print(f"[{mon_id}] [IA] Analyse en cours (tentative {tentative+1}/{max_tentatives})...")
            
            reponse_llm = self._appeler_ollama(prompt, timeout=self.timeout_requete)

            if reponse_llm:
                # Extraction et validation du JSON
                analyse = self._extraire_json(reponse_llm)
                
                if analyse and self._valider_analyse(analyse):
                    # Normalisation de la confiance
                    analyse["confiance"] = self._normaliser_confiance(analyse["confiance"])
                    
                    print(f"[{mon_id}] [IA] Analyse réussie")
                    return analyse
                else:
                    print(f"[{mon_id}] [IA] JSON invalide, nouvelle tentative...")
            else:
                print(f"[{mon_id}] [IA] Pas de réponse, nouvelle tentative...")

        # Fallback : vote aléatoire si toutes les tentatives échouent
        print(f"[{mon_id}] [IA] Échec après {max_tentatives} tentatives, vote aléatoire")
        return self._vote_aleatoire(mon_id, list(temperatures_autres.keys()))

    def _vote_espion(self, mon_id, autres_capteurs):
        """
        Stratégie de vote de l'espion : vote aléatoire pour semer le doute.
        
        Args:
            mon_id: Identifiant du capteur espion
            autres_capteurs: Liste des autres capteurs
            
        Returns:
            dict: Vote formaté
        """
        # Vote sur un autre capteur au hasard
        capteurs_disponibles = [c for c in autres_capteurs if c != mon_id]
        suspect = random.choice(capteurs_disponibles) if capteurs_disponibles else "rpi1"
        
        print(f"[{mon_id}] [ESPION] Vote stratégique (désinformation) : {suspect}")
        
        return {
            "suspect": suspect,
            "confiance": 0.85,  # Confiance élevée pour paraître crédible
            "preuves": ["Vote stratégique de désinformation"],
            "analyse_comparative": "Tentative de manipulation du vote collectif"
        }

    def _vote_aleatoire(self, mon_id, capteurs_disponibles):
        """
        Vote de secours si l'IA est indisponible.
        
        Args:
            mon_id: Identifiant du capteur courant
            capteurs_disponibles: Liste des capteurs participant au vote
            
        Returns:
            dict: Vote formaté
        """
        autres = [c for c in capteurs_disponibles if c != mon_id]
        suspect = random.choice(autres) if autres else "rpi1"
        
        print(f"[{mon_id}] [SECOURS] Vote aléatoire (IA indisponible) : {suspect}")
        
        return {
            "suspect": suspect,
            "confiance": 0.25,  # Confiance faible
            "preuves": ["Vote aléatoire de secours (IA indisponible)"],
            "analyse_comparative": "Aucune analyse disponible"
        }

    def _extraire_json(self, texte):
        """
        Extrait le JSON de la réponse du LLM.
        
        Args:
            texte: Réponse brute du LLM
            
        Returns:
            dict: Objet JSON parsé ou None
        """
        # Recherche du premier '{' et du dernier '}'
        debut = texte.find('{')
        fin = texte.rfind('}')
        
        if debut != -1 and fin != -1 and fin > debut:
            json_str = texte[debut:fin+1]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"[IA] Erreur JSON : {e}")
                return None
        
        print("[IA] Aucun JSON trouvé dans la réponse")
        return None

    def _valider_analyse(self, analyse):
        """
        Valide qu'une analyse contient tous les champs requis.
        
        Args:
            analyse: Dictionnaire à valider
            
        Returns:
            bool: True si valide, False sinon
        """
        if not isinstance(analyse, dict):
            print("[IA] L'analyse n'est pas un dictionnaire")
            return False
        
        # Vérification du champ "suspect"
        if "suspect" not in analyse:
            print("[IA] Champ 'suspect' manquant")
            return False
        
        suspect = analyse["suspect"]
        if not isinstance(suspect, str) or not suspect.startswith("rpi"):
            print(f"[IA] 'suspect' invalide : {suspect}")
            return False
        
        # Vérification du champ "confiance"
        if "confiance" not in analyse:
            print("[IA] Champ 'confiance' manquant")
            return False
        
        # Ajout de valeurs par défaut pour les champs optionnels
        if "preuves" not in analyse:
            analyse["preuves"] = ["Analyse du LLM"]
        
        if "analyse_comparative" not in analyse:
            analyse["analyse_comparative"] = "Analyse effectuée par le LLM"
        
        return True

    def _normaliser_confiance(self, confiance):
        """
        Normalise la confiance entre 0.0 et 1.0.
        
        Args:
            confiance: Valeur de confiance (peut être str, float, int)
            
        Returns:
            float: Confiance normalisée entre 0.0 et 1.0
        """
        try:
            # Cas où la confiance est une chaîne (ex: "85%" ou "0.85")
            if isinstance(confiance, str):
                confiance = confiance.replace('%', '').replace(',', '.').strip()
                confiance = float(confiance)
                
                # Si >1, c'est probablement un pourcentage
                if confiance > 1:
                    confiance /= 100.0
            
            # Conversion en float
            confiance = float(confiance)
            
            # Clipping entre 0.0 et 1.0
            return max(0.0, min(1.0, confiance))
            
        except (ValueError, TypeError) as e:
            print(f"[IA] Erreur normalisation confiance : {e}, défaut=0.5")
            return 0.5



class CapteurTemperature:
    """
    Capteur de température IoT avec détection d'espion par IA.
    Compatible avec ServeurArbitre.
    """

    def __init__(self, capteur_id, broker_address="10.109.150.133", broker_port=1883):
        self.capteur_id = capteur_id
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client(capteur_id)

        # Configuration réseau
        self.mon_ip = self.obtenir_ip_locale()

        # Données du jeu
        self.role = None
        self.ma_latitude = None
        self.ma_longitude = None
        self.capteurs_ids = []  # CORRECTION : Liste simple
        self.villes_coords = {}  # CORRECTION : Format du serveur
        self.capteurs_ips = {}
        self.config_recue = False
        self.role_recu = False

        # Collecte des données
        self.temperatures_recues = defaultdict(list)
        self.mes_temperatures_publiees = []
        self.nb_publications = 0
        self.MAX_PUBLICATIONS = 5

        # Générateur espion
        self.generateur_espion = GenerateurTemperatureEspion(
            moyenne=10.0,
            ecart_type=3.5,
            min_temp=-10.0,
            max_temp=30.0
        )

        # Agent IA
        self.analyseur = AnalyseurIA(ollama_url="http://10.103.1.12:11434")

        # Synchronisation
        self.lock = threading.Lock()
        self.publication_terminee = False

        # Callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def obtenir_ip_locale(self):
        """Récupère l'adresse IP locale."""
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "IP inconnue"

    def on_connect(self, client, userdata, flags, rc):
        """Callback appelé lors de la connexion au broker MQTT."""
        if rc == 0:
            print(f"[{self.capteur_id}] Connecté au broker MQTT")
            
            # Abonnements
            client.subscribe("iot/config", qos=1)
            client.subscribe(f"iot/role/{self.capteur_id}", qos=1)
            client.subscribe("iot/capteurs/+/temperature", qos=1)
            
            # Publication de présence
            presence_msg = json.dumps({
                "ip": self.mon_ip,
                "timestamp": time.time()
            })
            client.publish(
                f"iot/capteurs/{self.capteur_id}/presence",
                presence_msg,
                qos=1,
                retain=True
            )
            
            print(f"[{self.capteur_id}] En attente de configuration...")
        else:
            print(f"[{self.capteur_id}] Échec de connexion : code {rc}")

    def on_message(self, client, userdata, msg):
        """Callback appelé lors de la réception d'un message MQTT."""
        if len(msg.payload) == 0:
            return
        
        topic = msg.topic
        
        try:
            if topic == "iot/config":
                self.traiter_configuration(msg.payload)
            elif topic == f"iot/role/{self.capteur_id}":
                self.traiter_role(msg.payload)
            elif topic.startswith("iot/capteurs/") and topic.endswith("/temperature"):
                capteur_source = topic.split('/')[2]
                if capteur_source != self.capteur_id:
                    self.traiter_temperature_recue(capteur_source, msg.payload)
        except Exception as e:
            print(f"[{self.capteur_id}] Erreur traitement message : {e}")

    def traiter_configuration(self, payload):
        """Traite la configuration envoyée par le serveur."""
        try:
            config = json.loads(payload.decode())
            
            with self.lock:
                # CORRECTION : Adapter au format du serveur
                self.capteurs_ids = config["capteurs"]  # Liste simple
                self.villes_coords = config["villes_coords"]  # Dict {rpi_id: (lat, lon)}
                self.capteurs_ips = config.get("capteurs_ips", {})
                self.config_recue = True

            # Trouver mes coordonnées
            if self.capteur_id in self.villes_coords:
                self.ma_latitude, self.ma_longitude = self.villes_coords[self.capteur_id]
                print(f"[{self.capteur_id}] Configuration reçue")
                print(f"[{self.capteur_id}] Position : lat={self.ma_latitude}, lon={self.ma_longitude}")

            self.demarrer_si_pret()

        except Exception as e:
            print(f"[{self.capteur_id}] Erreur configuration : {e}")

    def traiter_role(self, payload):
        """Traite l'attribution du rôle."""
        try:
            role_data = json.loads(payload.decode())
            
            with self.lock:
                self.role = role_data["role"]
                self.role_recu = True

            if self.role == "espion":
                print(f"[{self.capteur_id}] ========================================")
                print(f"[{self.capteur_id}] RÔLE : ESPION")
                print(f"[{self.capteur_id}] ========================================")
            else:
                print(f"[{self.capteur_id}] Rôle : Capteur normal")

            self.demarrer_si_pret()

        except Exception as e:
            print(f"[{self.capteur_id}] Erreur traitement rôle : {e}")

    def demarrer_si_pret(self):
        """Démarre si configuration et rôle reçus."""
        with self.lock:
            if self.config_recue and self.role_recu:
                print(f"[{self.capteur_id}] Démarrage dans 3s...")
                threading.Thread(target=self._demarrer_apres_delai, daemon=True).start()

    def _demarrer_apres_delai(self):
        """Démarre après un délai."""
        time.sleep(3)
        self.publier_temperatures()

    def traiter_temperature_recue(self, capteur_source, payload):
        """Enregistre une température reçue."""
        try:
            data = json.loads(payload.decode())
            temperature = data["temperature"]

            with self.lock:
                self.temperatures_recues[capteur_source].append(temperature)
                
                if self.role == "espion" and len(self.temperatures_recues[capteur_source]) == 2:
                    self.ajuster_parametres_espion()

        except Exception as e:
            print(f"[{self.capteur_id}] Erreur réception température : {e}")

    def ajuster_parametres_espion(self):
        """Ajuste les paramètres de l'espion dynamiquement."""
        toutes_temperatures = []
        for temps in self.temperatures_recues.values():
            toutes_temperatures.extend(temps)

        if len(toutes_temperatures) > 0:
            moyenne_groupe = np.mean(toutes_temperatures)
            ecart_type_groupe = np.std(toutes_temperatures)
            
            self.generateur_espion.ajuster_parametres(moyenne_groupe, ecart_type_groupe)

    def obtenir_temperature(self):
        """Récupère une température selon le rôle."""
        if self.role == "espion":
            return self.generateur_espion.generer_temperature_aberrante()
        else:
            try:
                url = "https://api.open-meteo.com/v1/forecast"
                params = {
                    "latitude": self.ma_latitude,
                    "longitude": self.ma_longitude,
                    "current_weather": "true"
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    return round(response.json()["current_weather"]["temperature"], 1)
                return 10.0
            except:
                return 10.0

    def publier_temperatures(self):
        """Publie 5 températures espacées de 5 secondes."""
        print(f"\n[{self.capteur_id}] {'='*60}")
        print(f"[{self.capteur_id}] PHASE DE PUBLICATION")
        print(f"[{self.capteur_id}] {'='*60}\n")

        for i in range(self.MAX_PUBLICATIONS):
            temperature = self.obtenir_temperature()

            with self.lock:
                self.mes_temperatures_publiees.append(temperature)

            message = json.dumps({
                "temperature": temperature,
                "timestamp": time.time(),
                "publication_num": i + 1
            })

            self.client.publish(
                f"iot/capteurs/{self.capteur_id}/temperature",
                message,
                qos=1
            )

            marqueur = "[ESPION]" if self.role == "espion" else ""
            print(f"[{self.capteur_id}] {marqueur} Publication {i+1}/5 : {temperature}°C")

            if i < self.MAX_PUBLICATIONS - 1:
                time.sleep(5)

        with self.lock:
            self.publication_terminee = True

        print(f"\n[{self.capteur_id}] Publications terminées\n")
        time.sleep(3)
        self.analyser_et_voter()

    def analyser_et_voter(self):
        """Analyse et vote."""
        print(f"[{self.capteur_id}] {'='*60}")
        print(f"[{self.capteur_id}] PHASE D'ANALYSE AVEC IA")
        print(f"[{self.capteur_id}] {'='*60}\n")

        with self.lock:
            mes_temps = self.mes_temperatures_publiees.copy()
            autres_temps = dict(self.temperatures_recues)
            je_suis_espion = (self.role == "espion")

        analyse = self.analyseur.analyser_espion(
            self.capteur_id,
            mes_temps,
            autres_temps,
            self.capteurs_ips,
            je_suis_espion
        )

        print(f"[{self.capteur_id}] Suspect : {analyse['suspect']}")
        print(f"[{self.capteur_id}] Confiance : {analyse['confiance']:.0%}\n")

        self.voter(analyse['suspect'])

    def voter(self, suspect_id):
        """Envoie un vote au serveur."""
        vote_message = json.dumps({
            "suspect": suspect_id,
            "timestamp": time.time()
        })
        
        self.client.publish(f"iot/votes/{self.capteur_id}", vote_message, qos=1)
        print(f"[{self.capteur_id}] Vote envoyé : {suspect_id}\n")

    def executer(self):
        """Lance l'exécution du capteur."""
        print(f"[{self.capteur_id}] Démarrage du capteur")
        print(f"[{self.capteur_id}] IP : {self.mon_ip}\n")

        try:
            self.client.connect(self.broker_address, self.broker_port, 60)
            self.client.loop_forever()
        except KeyboardInterrupt:
            print(f"\n[{self.capteur_id}] Arrêt")
            self.client.disconnect()
        except Exception as e:
            print(f"[{self.capteur_id}] Erreur : {e}")
            self.client.disconnect()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python3 capteur.py <id_capteur>")
        print("Exemple : python3 capteur.py rpi1")
        sys.exit(1)

    capteur_id = sys.argv[1]
    
    if capteur_id not in ["rpi1", "rpi2", "rpi3", "rpi4"]:
        print("ID invalide. Utilisez : rpi1, rpi2, rpi3 ou rpi4")
        sys.exit(1)

    capteur = CapteurTemperature(capteur_id)
    capteur.executer()
