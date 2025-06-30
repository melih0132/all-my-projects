# Renommeur de Fichiers MP3 Intelligent - Analyse en Lot

Un script Python intelligent pour renommer automatiquement vos fichiers MP3 selon un format standardisé :

```
Artiste - Titre ft. Featuring.mp3
```

## Nouvelle Approche : Analyse en Lot

**Version 2.0** : Le script adopte une approche innovante d'analyse en lot :

1. **Extraction des titres** : Tous les titres des morceaux présents dans le dossier sont collectés.
2. **Analyse IA en lot** : L'IA analyse TOUS les fichiers en une seule requête.
3. **Recherche et identification** : L'IA utilise sa base de connaissances pour identifier chaque morceau.
4. **Extraction des informations** : Les informations nécessaires sont extraites pour chaque morceau identifié.
5. **Reformatage des titres** : Les titres sont reformattés selon le format standard.
6. **Attribution des noms** : Les noms reformatés sont attribués aux fichiers du dossier.

### Avantages de l'approche en lot

- **Plus rapide** : Une seule requête IA au lieu d'une par fichier.
- **Plus précis** : L'IA identifie les vrais titres grâce à sa base de connaissances.
- **Plus cohérent** : Analyse globale pour éviter les incohérences.
- **Plus économique** : Moins d'appels API = coûts réduits.
- **Plus robuste** : Fallback automatique en cas d'échec de l'IA.

## Outils inclus

### 1. rename_music.py - Renommeur intelligent principal
- **Analyse en lot** : Tous les fichiers traités en une seule requête IA.
- **Parsing intelligent** : Extraction automatique de l'artiste, du titre et des featuring.
- **Support des tags ID3** : Utilisation prioritaire des métadonnées MP3 si disponibles.
- **Mode IA avancé** : Intégration avec OpenAI GPT pour une analyse plus précise.
- **Multilingue** : Support du français, anglais, turc et autres langues.
- **Gestion des conflits** : Évite automatiquement les doublons de noms.
- **Mode test** : Possibilité de simuler les changements sans modifier les fichiers.
- **Robuste** : Gestion avancée des erreurs et compatibilité Windows/Linux/Mac.

### 2. clean_filenames.py - Nettoyeur de suffixes numériques
- **Suppression automatique** des suffixes comme " (1)", " (2)", etc.
- **Détection intelligente** des patterns numériques en fin de nom.
- **Gestion des conflits** : Évite les doublons lors du nettoyage.
- **Mode simulation** : Test sans modification des fichiers.
- **Rapport détaillé** : Statistiques complètes du traitement.

## Installation

### Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Dépendances

Installez toutes les dépendances avec :
```bash
pip install -r requirements.txt
```

Ou installez manuellement :
```bash
pip install mutagen openai python-dotenv
```

### Configuration IA

**Obligatoire pour rename_music.py** :

1. Créez un fichier `.env` dans le même répertoire que le script :
   ```
   OPENAI_API_KEY=votre-clé-api-openai
   ```
2. Ou définissez la variable d'environnement :
   ```bash
   export OPENAI_API_KEY="votre-clé-api-openai"
   ```

## Utilisation

### rename_music.py - Renommeur intelligent

```bash
# Renommer tous les fichiers MP3 du répertoire courant
python rename_music.py

# Spécifier un répertoire
python rename_music.py /chemin/vers/musique

# Mode test (affiche les changements sans les appliquer)
python rename_music.py --dry-run

# Mode verbose (affiche les détails)
python rename_music.py --verbose

# Limiter le nombre de fichiers traités
python rename_music.py --limit 10
```

### clean_filenames.py - Nettoyeur de suffixes

```bash
# Nettoyer les suffixes numériques dans le répertoire courant
python clean_filenames.py

# Spécifier un répertoire
python clean_filenames.py /chemin/vers/musique

# Mode test
python clean_filenames.py --dry-run

# Affichage détaillé
python clean_filenames.py --verbose
```

### Options disponibles

**rename_music.py** :
- `--dry-run` : Affiche les changements sans les appliquer
- `--verbose, -v` : Affiche les détails du traitement
- `--limit N` : Limite le traitement aux N premiers fichiers
- `--help` : Affiche l'aide complète

**clean_filenames.py** :
- `--dry-run` : Mode simulation sans modification
- `--verbose, -v` : Affichage détaillé des informations
- `--help` : Affiche l'aide complète

### Exemples d'utilisation

```bash
# Tester le renommeur sur 5 fichiers
python rename_music.py --dry-run --limit 5 --verbose

# Nettoyer les suffixes numériques
python clean_filenames.py --dry-run --verbose

# Traitement complet avec les deux outils
python clean_filenames.py --verbose
python rename_music.py --verbose
```

## Formats supportés

Le script peut analyser et renommer des fichiers avec des noms comme :

- `Artiste - Titre.mp3`
- `Artiste - Titre ft. Featuring.mp3`
- `Artiste - Titre (Official Video).mp3`
- `Artiste - Titre [Audio].mp3`
- `Artiste - Titre feat. Featuring.mp3`
- `Artiste x Featuring - Titre.mp3`
- `Titre incomplet ou mal formaté.mp3` → L'IA identifiera le vrai titre
- `Fichier (1).mp3` → `Fichier.mp3` (nettoyage des suffixes)

## Méthodes d'analyse

### 1. Analyse IA en lot (nouvelle approche)
- **Une seule requête** pour tous les fichiers
- **Base de connaissances** de l'IA pour identifier les vrais titres
- **Analyse contextuelle** entre les fichiers
- **Fallback automatique** en cas d'échec

### 2. Tags ID3 (priorité si disponibles)
Si les métadonnées MP3 contiennent les informations artiste/titre, elles sont utilisées en priorité.

### 3. Règles de fallback
Algorithme avancé basé sur des règles pour extraire les informations :
- Détection des séparateurs (-, –, —)
- Reconnaissance des featuring (ft, feat, featuring, &, x)
- Nettoyage des suffixes (Official Video, Audio, etc.)
- Capitalisation intelligente

## Format de sortie

Tous les fichiers sont renommés selon le format standardisé :
```
Artiste - Titre.mp3
Artiste - Titre ft. Featuring.mp3
```

## Gestion des erreurs

Les scripts gèrent automatiquement :
- Fichiers introuvables
- Conflits de noms (ajout automatique de numéros)
- Permissions insuffisantes
- Encodages problématiques
- Caractères spéciaux
- Échecs de l'IA (fallback automatique)

## Statistiques

Les scripts affichent un rapport détaillé incluant :
- Nombre de fichiers traités
- Fichiers renommés avec succès
- Fichiers ignorés (déjà au bon format)
- Erreurs rencontrées
- Succès de l'IA en lot
- Utilisation du fallback
- Temps de traitement

## Compatibilité

- **Systèmes d'exploitation** : Windows, Linux, macOS
- **Encodages** : UTF-8, gestion automatique des accents
- **Fichiers** : MP3 avec ou sans tags ID3
- **Noms de fichiers** : Support des caractères spéciaux et accents

## Sécurité

- Mode test disponible pour vérifier les changements
- Sauvegarde recommandée avant traitement en masse
- Gestion sécurisée des noms de fichiers
- Validation des chemins et permissions
- Fallback automatique en cas d'échec IA

## Dépannage

### Erreurs courantes

1. **"mutagen non installé"** : Installez avec `pip install mutagen`
2. **"openai non installé"** : Installez avec `pip install openai` (recommandé)
3. **"OPENAI_API_KEY non trouvée"** : Créez un fichier `.env` avec votre clé API
4. **"Permission refusée"** : Vérifiez les droits d'accès au répertoire
5. **"Fichier introuvable"** : Le fichier a peut-être été déplacé ou supprimé

### Conseils

- Testez toujours avec `--dry-run` avant un traitement en masse
- Utilisez `--limit` pour tester sur un petit nombre de fichiers
- Activez `--verbose` pour diagnostiquer les problèmes
- Sauvegardez vos fichiers avant traitement
- L'approche en lot est plus rapide et plus précise

## Changements majeurs v2.0

- **Analyse en lot** : Une seule requête IA pour tous les fichiers
- **Base de connaissances** : L'IA utilise ses connaissances pour identifier les vrais titres
- **Performance améliorée** : Traitement plus rapide et économique
- **Fallback robuste** : Gestion automatique des échecs IA
- **Statistiques détaillées** : Suivi des succès IA et fallback
- **Nouvel outil** : clean_filenames.py pour le nettoyage des suffixes

## Licence

Ce script est fourni en l'état, sans garantie. Utilisez-le à vos propres risques.

## Contribution

Les suggestions d'amélioration et les rapports de bugs sont les bienvenus.