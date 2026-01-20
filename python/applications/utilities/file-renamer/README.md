# Formatage de Titres Musicaux - Version Refactorisée

Un script Python intelligent pour reformater automatiquement les noms de fichiers musicaux selon un format standardisé :

```
Artiste - Titre ft. Featuring.mp3
```

## Description

Ce module propose une solution complète de formatage de titres musicaux avec une architecture orientée objet, séparation des responsabilités et optimisation des performances. Le script analyse les noms de fichiers existants, extrait les informations (artiste principal, titre, featuring), nettoie les mentions indésirables et reformate selon un standard cohérent.

## Caractéristiques principales

- **Architecture modulaire** : Séparation claire des responsabilités (parsing, nettoyage, formatage, système de fichiers)
- **Traitement parallèle** : Support du traitement multi-thread pour améliorer les performances
- **Cache LRU** : Mise en cache des résultats pour éviter les recalculs
- **Configuration flexible** : Support de fichiers de configuration JSON personnalisés
- **Gestion robuste des erreurs** : Gestion complète des cas limites et erreurs système
- **Mode simulation** : Possibilité de tester les changements sans modifier les fichiers
- **Traitement récursif** : Support du traitement des sous-dossiers
- **Multi-formats** : Support de nombreux formats audio (MP3, WAV, FLAC, M4A, AAC, OGG, WMA, OPUS)
- **Logging complet** : Journalisation détaillée des opérations

## Installation

### Prérequis

- Python 3.7 ou supérieur
- Aucune dépendance externe requise (utilise uniquement la bibliothèque standard)

### Installation

Aucune installation de dépendances n'est nécessaire. Le script utilise uniquement les modules de la bibliothèque standard Python.

## Utilisation

### Utilisation de base

```bash
# Traiter les fichiers du répertoire courant (mode simulation par défaut)
python music_formatter.py --verbose

# Appliquer les changements réellement
python music_formatter.py

# Traitement récursif des sous-dossiers
python music_formatter.py --recursive

# Désactiver le traitement parallèle
python music_formatter.py --no-parallel
```

### Options disponibles

- `--verbose, -v` : Mode simulation (affiche les changements sans les appliquer)
- `--recursive, -r` : Traitement récursif des sous-dossiers
- `--config` : Spécifier un fichier de configuration JSON personnalisé
- `--parallel` : Activer le traitement parallèle (activé par défaut)
- `--no-parallel` : Désactiver le traitement parallèle
- `--workers N` : Nombre de workers pour le traitement parallèle (défaut: 4)
- `--create-config` : Créer un fichier de configuration d'exemple
- `--backup` : Créer une sauvegarde des noms de fichiers avant traitement
- `--help` : Afficher l'aide complète

### Exemples d'utilisation

```bash
# Tester les changements sans les appliquer
python music_formatter.py --verbose

# Traiter récursivement avec traitement parallèle
python music_formatter.py --recursive --workers 8

# Créer un fichier de configuration personnalisé
python music_formatter.py --create-config

# Traiter avec sauvegarde et configuration personnalisée
python music_formatter.py --backup --config music_formatter_config.json
```

## Configuration

Le script peut utiliser un fichier de configuration JSON pour personnaliser les patterns de nettoyage, les séparateurs d'artistes, les extensions supportées, etc.

### Créer un fichier de configuration

```bash
python music_formatter.py --create-config
```

Cela crée un fichier `music_formatter_config.json` avec la configuration par défaut que vous pouvez modifier.

### Structure de configuration

```json
{
  "cleanup_patterns": [
    "\\s*\\(Official Audio\\)",
    "\\s*\\(Official Video\\)"
  ],
  "feat_patterns": [
    "\\s*\\(\\s*(feat\\.?|featuring|ft\\.?)\\s+([^)]+)\\)"
  ],
  "artist_separators": ["\\s*&\\s*", "\\s*x\\s*", "\\s*,\\s*"],
  "music_extensions": [".mp3", ".wav", ".flac", ".m4a"],
  "title_case_exceptions": ["a", "an", "the", "and", "or"]
}
```

## Formats supportés

Le script peut analyser et reformater des fichiers avec des noms comme :

- `Artiste - Titre.mp3`
- `Artiste - Titre ft. Featuring.mp3`
- `Artiste - Titre (Official Video).mp3`
- `Artiste - Titre [Audio].mp3`
- `Artiste - Titre feat. Featuring.mp3`
- `Artiste x Featuring - Titre.mp3`
- `Artiste & Featuring - Titre.mp3`
- `01 Artiste - Titre.mp3` (suppression des numéros de piste)

## Format de sortie

Tous les fichiers sont reformatés selon le format standardisé :

```
Artiste - Titre.mp3
Artiste - Titre ft. Featuring.mp3
```

Les règles de formatage incluent :
- Suppression des mentions indésirables (Official Video, HD, etc.)
- Extraction et formatage des featuring
- Capitalisation intelligente (Title Case)
- Nettoyage des séparateurs multiples
- Suppression des numéros de piste

## Architecture

Le module est organisé en plusieurs classes spécialisées :

- **PatternCompiler** : Compilation et gestion des patterns regex
- **TitleCleaner** : Nettoyage des titres (suppression des mentions indésirables)
- **ArtistExtractor** : Extraction et traitement des artistes
- **TitleParser** : Parsing complet de la structure d'un titre
- **MusicTitleFormatter** : Formatage principal avec cache LRU
- **FileSystemHandler** : Opérations sur le système de fichiers
- **MusicFileProcessor** : Orchestration du traitement des fichiers

## Gestion des erreurs

Le script gère automatiquement :
- Fichiers introuvables ou permissions insuffisantes
- Conflits de noms (détection et avertissement)
- Chemins trop longs (limite Windows)
- Caractères invalides dans les noms de fichiers
- Erreurs de formatage (fallback sur le nom original)
- Timeouts lors du traitement parallèle

## Statistiques

Le script affiche un rapport détaillé incluant :
- Nombre de fichiers trouvés
- Fichiers traités avec succès
- Fichiers renommés
- Erreurs rencontrées
- Statistiques de cache (cache hits)
- Erreurs de formatage

## Compatibilité

- **Systèmes d'exploitation** : Windows, Linux, macOS
- **Encodages** : UTF-8, gestion automatique des accents
- **Fichiers** : MP3, WAV, FLAC, M4A, AAC, OGG, WMA, OPUS
- **Noms de fichiers** : Support des caractères spéciaux et accents
- **Python** : 3.7+

## Sécurité

- Mode simulation disponible pour vérifier les changements
- Sauvegarde optionnelle des noms de fichiers avant traitement
- Gestion sécurisée des noms de fichiers (sanitization)
- Validation des chemins et permissions
- Gestion des cas limites (chemins trop longs, caractères invalides)

## Logging

Le script génère un fichier de log `music_formatter.log` dans le répertoire courant avec :
- Les opérations de renommage effectuées
- Les erreurs rencontrées
- Les avertissements (conflits, chemins trop longs, etc.)

## Dépannage

### Erreurs courantes

1. **"Le dossier n'existe pas"** : Vérifiez que le chemin spécifié est correct
2. **"Permission refusée"** : Vérifiez les droits d'accès au répertoire
3. **"Chemin trop long"** : Le nom de fichier résultant dépasse la limite Windows (260 caractères)
4. **"Fichier existe déjà"** : Un fichier avec le même nom existe déjà (non renommé pour éviter les conflits)

### Conseils

- Testez toujours avec `--verbose` avant un traitement en masse
- Utilisez `--backup` pour créer une sauvegarde avant traitement
- Activez le logging pour diagnostiquer les problèmes
- Personnalisez la configuration selon vos besoins
- Le traitement parallèle améliore les performances sur de gros volumes

## Améliorations de la version refactorisée

- **Architecture modulaire** : Code mieux organisé et maintenable
- **Performance optimisée** : Cache LRU et traitement parallèle
- **Gestion d'erreurs robuste** : Gestion complète des cas limites
- **Configuration flexible** : Support de fichiers de configuration personnalisés
- **Logging détaillé** : Journalisation complète des opérations
- **Type hints** : Meilleure lisibilité et support IDE
- **Séparation des responsabilités** : Chaque classe a un rôle bien défini

## Licence

Ce script est fourni en l'état, sans garantie. Utilisez-le à vos propres risques.

## Contribution

Les suggestions d'amélioration et les rapports de bugs sont les bienvenus.
